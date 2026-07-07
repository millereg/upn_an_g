from django.shortcuts import render, redirect
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.utils import timezone
from calendar import month_abbr
from apps.ventas.models import Venta
from apps.compras.models import Compra
from apps.inventario.models import Inventario, Movimiento
from apps.productos.models import Producto, Lote


def index(request):
    user = request.user
    today = timezone.now().date()

    is_admin_or_dev = user.groups.filter(name__in=['Administrador', 'Desarrollador']).exists()
    is_vendedor = user.groups.filter(name='Vendedor').exists()
    is_almacenero = user.groups.filter(name='Almacenero').exists()

    context = {
        'is_admin_or_dev': is_admin_or_dev,
        'is_vendedor': is_vendedor,
        'is_almacenero': is_almacenero,
    }

    if is_admin_or_dev or is_vendedor:
        context['total_ventas'] = Venta.objects.count()
        context['ventas_hoy'] = Venta.objects.filter(fecha_creacion__date=today).count()
        context['ventas_mes'] = Venta.objects.filter(fecha_creacion__month=today.month, fecha_creacion__year=today.year).count()
        context['total_compras'] = Compra.objects.count()

    if is_admin_or_dev or is_almacenero:
        context['total_stock'] = Inventario.objects.aggregate(total=Sum('cantidad'))['total'] or 0
        context['total_lotes'] = Lote.objects.count()
        context['lotes_activos'] = Lote.objects.filter(estado='activo').count()
        context['movimientos_hoy'] = Movimiento.objects.filter(fecha__date=today).count()

    if is_admin_or_dev:
        context['total_usuarios'] = User.objects.count()
        context['total_productos'] = Producto.objects.count()
        context['productos_activos'] = Producto.objects.filter(estado='activo').count()
        context['stock_bajo'] = Inventario.objects.filter(cantidad__lt=10).count()

    movimientos_mes = Movimiento.objects.filter(
        fecha__year=today.year
    ).values('fecha__month').annotate(total=Count('id'))
    mov_data = [0] * 12
    for m in movimientos_mes:
        mov_data[m['fecha__month'] - 1] = m['total']
    context['movimientos_chart_data'] = mov_data

    lotes_estado = Lote.objects.values('estado').annotate(total=Count('id'))
    lotes_data = {'activo': 0, 'bloqueado': 0, 'vencido': 0, 'cuarentena': 0}
    for l in lotes_estado:
        if l['estado'] in lotes_data:
            lotes_data[l['estado']] = l['total']
    context['lotes_chart_data'] = lotes_data

    ventas_mes = Venta.objects.filter(
        fecha_creacion__year=today.year
    ).values('fecha_creacion__month').annotate(total=Count('id'))
    vent_data = [0] * 12
    for v in ventas_mes:
        vent_data[v['fecha_creacion__month'] - 1] = v['total']
    context['ventas_chart_data'] = vent_data

    meses_labels = [month_abbr[i] for i in range(1, 13)]
    context['meses_labels'] = meses_labels

    return render(request, 'dashboard/index.html', context)


def buscar(request):
    tipo = request.GET.get('tipo', '')
    q = request.GET.get('q', '').strip()

    if not q:
        return redirect('dashboard:index')

    urls = {
        'productos': '/productos/producto/',
        'lotes': '/productos/lote/',
        'categorias': '/productos/categoria/',
        'ventas': '/ventas/venta/',
        'compras': '/compras/compra/',
        'proveedores': '/compras/proveedor/',
        'almacenes': '/sucursales/almacen/',
        'sucursales': '/sucursales/sucursal/',
        'usuarios': '/usuarios/usuario/',
    }

    if tipo in urls:
        return redirect(f'{urls[tipo]}?q={q}')

    return redirect('dashboard:index')