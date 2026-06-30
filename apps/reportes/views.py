from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.inventario.models import Inventario
from apps.productos.models import Producto
from apps.compras.models import Proveedor
from apps.sucursales.models import Almacen


@login_required
def reorder_point_report(request):
    inventarios = Inventario.objects.select_related('almacen', 'lote__producto').all()

    reorder_list = []
    for inv in inventarios:
        stock = inv.cantidad
        punto_reorden = getattr(inv, 'punto_reorden', 10)
        demanda = getattr(inv, 'demanda_historica', []) or []

        necesita_reorden = stock <= punto_reorden
        eoq = calcular_eoq(demanda)

        reorder_list.append({
            'producto': inv.lote.producto.nombre if inv.lote and inv.lote.producto else 'N/A',
            'lote': str(inv.lote) if inv.lote else 'N/A',
            'almacen': str(inv.almacen) if inv.almacen else 'N/A',
            'stock': stock,
            'punto_reorden': punto_reorden,
            'necesita_reorden': necesita_reorden,
            'eoq': eoq,
        })

    context = {
        'reorder_list': reorder_list,
        'title': 'Reporte - Punto de Reorden'
    }
    return render(request, 'reportes/reorder_point.html', context)


def calcular_eoq(demandaHistorica):
    if not demandaHistorica or len(demandaHistorica) < 3:
        return 0
    demanda = sum(demandaHistorica[-12:])
    costo_orden = 10
    costo_hold = 0.5
    if demanda == 0:
        return 0
    eoq = int((2 * demanda * costo_orden / costo_hold) ** 0.5)
    return eoq


@login_required
def asignacion_almacenes_report(request):
    productos = Producto.objects.filter(estado='activo').select_related('categoria')
    inventarios = Inventario.objects.select_related('almacen', 'lote__producto').all()
    almacenes = Almacen.objects.all()

    almacenes_info = {alm.id: {'nombre': str(alm), 'capacidad': alm.capacidad} for alm in almacenes}

    stock_por_almacen = {}
    for inv in inventarios:
        alm_id = inv.almacen_id
        if alm_id not in stock_por_almacen:
            stock_por_almacen[alm_id] = 0
        stock_por_almacen[alm_id] += inv.cantidad

    producto_almacen_map = {}
    for inv in inventarios:
        producto_nombre = inv.lote.producto.nombre if inv.lote and inv.lote.producto else None
        if producto_nombre:
            if producto_nombre not in producto_almacen_map:
                producto_almacen_map[producto_nombre] = []
            producto_almacen_map[producto_nombre].append({
                'almacen_id': inv.almacen_id,
                'almacen_nombre': str(inv.almacen),
                'cantidad': inv.cantidad,
            })

    asignaciones = []
    for producto in productos:
        cantidad_total = 0
        for inv in inventarios:
            if inv.lote and inv.lote.producto and inv.lote.producto.id == producto.id:
                cantidad_total += inv.cantidad

        mejor_almacen_nombre = 'Sin asignar'
        mejor_almacen_disponible = 0
        mejor_almacen_capacidad = 0
        if producto.nombre in producto_almacen_map:
            for alm_data in producto_almacen_map[producto.nombre]:
                alm_id = alm_data['almacen_id']
                capacidad = almacenes_info.get(alm_id, {}).get('capacidad', 0)
                usado = stock_por_almacen.get(alm_id, 0)
                disponible = capacidad - usado
                if disponible >= mejor_almacen_disponible:
                    mejor_almacen_disponible = disponible
                    mejor_almacen_nombre = alm_data['almacen_nombre']
                    mejor_almacen_capacidad = capacidad

        asignaciones.append({
            'producto': producto.nombre,
            'categoria': str(producto.categoria) if producto.categoria else 'N/A',
            'stock_total': cantidad_total,
            'almacen_asignado': mejor_almacen_nombre,
            'capacidad': mejor_almacen_capacidad,
            'disponible': mejor_almacen_disponible,
        })

    context = {
        'asignaciones': asignaciones,
        'title': 'Reporte - Asignación de Almacenes'
    }
    return render(request, 'reportes/asignacion_almacenes.html', context)


@login_required
def planification_purchases_report(request):
    inventarios = Inventario.objects.select_related('almacen', 'lote__producto').all()
    proveedores = Proveedor.objects.all()

    productos_bajos = []
    for inv in inventarios:
        punto_reorden = getattr(inv, 'punto_reorden', 10)
        if inv.cantidad <= punto_reorden:
            productos_bajos.append({
                'producto': inv.lote.producto.nombre if inv.lote and inv.lote.producto else 'N/A',
                'lote': str(inv.lote),
                'stock_actual': inv.cantidad,
                'punto_reorden': punto_reorden,
                'cantidad_necesaria': max(0, punto_reorden - inv.cantidad + 10),
            })

    proveedores_productos = {}
    for prov in proveedores:
        proveedores_productos[prov.nombre] = {
            'costo_unitario': 10,
            'capacidad': 1000,
        }

    sugerencias = programacion_dinamica_compras(productos_bajos, proveedores_productos)

    context = {
        'productos_bajos': productos_bajos,
        'sugerencias': sugerencias,
        'title': 'Reporte - Planificación de Compras'
    }
    return render(request, 'reportes/planificacion_compras.html', context)


def programacion_dinamica_compras(productos_bajos, proveedores):
    if not productos_bajos:
        return []

    sugerencias = []
    for prod in productos_bajos:
        cantidad = prod['cantidad_necesaria']
        mejor_opcion = None
        mejor_costo = float('inf')

        for prov_nombre, prov_data in proveedores.items():
            if prov_data['capacidad'] >= cantidad:
                costo = cantidad * prov_data['costo_unitario']
                if costo < mejor_costo:
                    mejor_costo = costo
                    mejor_opcion = prov_nombre

        sugerencias.append({
            'producto': prod['producto'],
            'cantidad_necesaria': cantidad,
            'proveedor': mejor_opcion or 'Sin opción',
            'costo_total': mejor_costo if mejor_opcion else 0,
        })

    return sugerencias


@login_required
def forecasting_report(request):
    productos = Producto.objects.filter(estado='activo').select_related('categoria')

    ventas_por_producto = {}
    for producto in productos:
        cantidad_total = 0
        detalles = producto.ventas_detalles.all() if hasattr(producto, 'ventas_detalles') else []
        for det in detalles:
            cantidad_total += det.cantidad
        ventas_por_producto[producto.id] = cantidad_total

    predicciones = []
    for producto in productos:
        hist = []
        for i in range(6):
            mes_key = f'mes_{i+1}'
            if hasattr(producto, mes_key):
                hist.append(getattr(producto, mes_key))

        if not hist:
            hist = [10, 12, 15, 14, 18, 20][:6]

        forecast = suavizado_exponencial(hist)

        predicciones.append({
            'producto': producto.nombre,
            'categoria': str(producto.categoria) if producto.categoria else 'N/A',
            'historico': hist,
            'forecast_3_meses': forecast * 3,
            'forecast_mes': forecast,
        })

    context = {
        'predicciones': predicciones,
        'title': 'Reporte - Pronóstico de Demanda'
    }
    return render(request, 'reportes/forecasting.html', context)


def suavizado_exponencial(historico, alpha=0.3):
    if not historico or len(historico) < 2:
        return 0

    forecast = historico[0]
    for valor in historico[1:]:
        forecast = alpha * valor + (1 - alpha) * forecast

    return int(forecast)


@login_required
def redistribucion_report(request):
    inventarios = Inventario.objects.select_related('almacen', 'lote__producto').all()
    almacenes = Almacen.objects.filter(estado='activo')

    # Crear dict con todos los almacenes
    stock_por_almacen = {}
    for alm in almacenes:
        stock_por_almacen[str(alm)] = {
            'total': 0,
            'productos': [],
            'capacidad': alm.capacidad,
            'uso_porcentaje': 0
        }

    # Llenar con datos de inventario
    for inv in inventarios:
        alm_nombre = str(inv.almacen) if inv.almacen else 'Unknown'
        if alm_nombre in stock_por_almacen:
            stock_por_almacen[alm_nombre]['total'] += inv.cantidad
            stock_por_almacen[alm_nombre]['productos'].append({
                'producto': inv.lote.producto.nombre if inv.lote and inv.lote.producto else 'N/A',
                'cantidad': inv.cantidad,
            })

    # Calcular uso %
    for alm_data in stock_por_almacen.values():
        capacidad = alm_data['capacidad']
        total = alm_data['total']
        alm_data['uso_porcentaje'] = int((total / capacidad) * 100) if capacidad > 0 else 0

    redistribuciones = calcular_redistribucion(stock_por_almacen)

    context = {
        'stock_por_almacen': stock_por_almacen,
        'redistribuciones': redistribuciones,
        'title': 'Reporte - Redistribución de Stock'
    }
    return render(request, 'reportes/redistribucion.html', context)


def calcular_redistribucion(stock_por_almacen):
    redistribuciones = []

    if not stock_por_almacen:
        return redistribuciones

    # Clasificar: >80% = congestionados, <50% = disponibles
    congestionados = []
    disponibles = []

    for alm_nombre, alm_data in stock_por_almacen.items():
        uso_pct = alm_data.get('uso_porcentaje', 0)
        capacidad = alm_data.get('capacidad', 1000)
        stock = alm_data.get('total', 0)

        if uso_pct > 80:
            congestionados.append({'nombre': alm_nombre, 'stock': stock, 'capacidad': capacidad, 'uso': uso_pct})
        elif uso_pct < 50:
            disponibles.append({'nombre': alm_nombre, 'stock': stock, 'capacidad': capacidad, 'uso': uso_pct})

    # Si no hay congestionados o disponibles, no hay redistribución
    if not congestionados or not disponibles:
        return redistribuciones

    # Sugerir mover stock desde congestionados hacia disponibles
    for cong in congestionados:
        excedente = int(cong['stock'] - cong['capacidad'] * 0.8)

        if excedente <= 0:
            continue

        for disp in disponibles:
            espacio = disp['capacidad'] - disp['stock']

            if espacio <= 0:
                continue

            cantidad = min(excedente, espacio)
            redistribuciones.append({
                'desde': cong['nombre'],
                'hacia': disp['nombre'],
                'cantidad': cantidad,
                'motivo': f'{cong["nombre"]} al {cong["uso"]}% → {disp["nombre"]} al {disp["uso"]}%',
            })
            break

    return redistribuciones
