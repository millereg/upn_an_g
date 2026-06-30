from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from django.db import models
from .models import Inventario, Movimiento, DetalleMovimiento
from .forms import MovimientoForm, DetalleMovimientoForm
from apps.sucursales.models import Almacen


def get_stock_actual(almacen):
    total = Inventario.objects.filter(almacen=almacen).aggregate(total=models.Sum('cantidad'))['total'] or 0
    return total


def verificar_capacidad(almacen, cantidad_a_agregar):
    stock_actual = get_stock_actual(almacen)
    capacidad = almacen.capacidad
    nuevo_stock = stock_actual + cantidad_a_agregar
    if nuevo_stock > capacidad:
        return False, stock_actual, capacidad
    return True, stock_actual, capacidad


def get_almacen_capacidades():
    almacenes = Almacen.objects.all()
    result = {}
    for alm in almacenes:
        stock = Inventario.objects.filter(almacen=alm).aggregate(total=models.Sum('cantidad'))['total'] or 0
        disponible = alm.capacidad - stock
        result[alm.id] = {
            'nombre': str(alm),
            'capacidad': alm.capacidad,
            'stock': stock,
            'disponible': max(0, disponible)
        }
    return result


@login_required
def inventario_list(request):
    inventario = (
        Inventario.objects.select_related("almacen", "lote__producto")
        .all()
        .order_by("-id")
    )
    q = request.GET.get('q', '').strip()
    if q:
        from apps.productos.models import Producto
        inventario = inventario.filter(lote__producto__nombre__icontains=q)

    for inv in inventario:
        capacidad = inv.almacen.capacidad if inv.almacen else 0
        stock_almacen = Inventario.objects.filter(almacen=inv.almacen).aggregate(total=models.Sum('cantidad'))['total'] or 0
        inv.capacidad_almacen = capacidad
        inv.stock_almacen_actual = stock_almacen
        inv.uso_porcentaje = int((stock_almacen / capacidad) * 100) if capacidad > 0 else 0

    return render(
        request, "inventario/inventario_list.html", {"inventario": inventario, "q": q}
    )


@login_required
def inventario_delete(request, id):
    inventario = get_object_or_404(Inventario, id=id)
    if request.method == "POST":
        inventario.delete()
    return redirect("inventario:inventario_list")


@login_required
def movimiento_list(request):
    movimientos = Movimiento.objects.select_related("almacen").all().order_by("-fecha")
    q = request.GET.get('q', '').strip()
    if q:
        movimientos = movimientos.filter(referencia__icontains=q)
    return render(
        request, "inventario/movimiento_list.html", {"movimientos": movimientos, "q": q}
    )


@login_required
def movimiento_create(request):
    DetalleFormSet = inlineformset_factory(
        Movimiento,
        DetalleMovimiento,
        form=DetalleMovimientoForm,
        extra=1,
        can_delete=True,
    )
    if request.method == "POST":
        form = MovimientoForm(request.POST)
        formset = DetalleFormSet(request.POST)
        if form.is_valid():
            if formset.is_valid():
                tipo = form.cleaned_data["tipo"]
                almacen = form.cleaned_data["almacen"]

                if tipo == "salida" or tipo == "transferencia":
                    for detalle_form in formset:
                        if (
                            detalle_form.cleaned_data.get("lote")
                            and detalle_form.cleaned_data.get("cantidad")
                            and not detalle_form.cleaned_data.get("DELETE")
                        ):
                            lote = detalle_form.cleaned_data["lote"]
                            cantidad = detalle_form.cleaned_data["cantidad"]
                            inv = Inventario.objects.filter(
                                almacen=almacen, lote=lote
                            ).first()
                            stock_actual = inv.cantidad if inv else 0
                            if cantidad > stock_actual:
                                messages.error(
                                    request,
                                    f"Stock insuficiente para {lote.numero_lote}. Stock actual: {stock_actual}",
                                )
                                return render(
                                    request,
                                    "inventario/movimiento_form.html",
                                    {
                                        "form": form,
                                        "detalle_formset": formset,
                                        "movimiento": None,
                                        "formset_errors": None,
                                        "almacen_capacidades": get_almacen_capacidades(),
                                    },
                                )

                if tipo == "entrada":
                    total_cantidad = sum(
                        detalle_form.cleaned_data.get("cantidad", 0)
                        for detalle_form in formset
                        if detalle_form.cleaned_data.get("lote")
                        and detalle_form.cleaned_data.get("cantidad")
                        and not detalle_form.cleaned_data.get("DELETE")
                    )
                    puede_agregar, stock_actual, capacidad = verificar_capacidad(almacen, total_cantidad)
                    if not puede_agregar:
                        messages.error(
                            request,
                            f"Almacén '{almacen.nombre}' sin capacidad. Stock: {stock_actual}, Capacidad: {capacidad}, Intentando agregar: {total_cantidad}"
                        )
                        return render(
                            request,
                            "inventario/movimiento_form.html",
                            {
                                "form": form,
                                "detalle_formset": formset,
                                "movimiento": None,
                                "formset_errors": None,
                                "almacen_capacidades": get_almacen_capacidades(),
                            },
                        )

                if tipo == "transferencia":
                    almacen_destino = form.cleaned_data.get("almacen_destino")
                    if almacen_destino:
                        total_cantidad = sum(
                            detalle_form.cleaned_data.get("cantidad", 0)
                            for detalle_form in formset
                            if detalle_form.cleaned_data.get("lote")
                            and detalle_form.cleaned_data.get("cantidad")
                            and not detalle_form.cleaned_data.get("DELETE")
                        )
                        puede_agregar, stock_actual, capacidad = verificar_capacidad(almacen_destino, total_cantidad)
                        if not puede_agregar:
                            messages.error(
                                request,
                                f"Almacén destino '{almacen_destino.nombre}' sin capacidad. Stock: {stock_actual}, Capacidad: {capacidad}, Intentando agregar: {total_cantidad}"
                            )
                            return render(
                                request,
                                "inventario/movimiento_form.html",
                                {
                                    "form": form,
                                    "detalle_formset": formset,
                                    "movimiento": None,
                                    "formset_errors": None,
                                    "almacen_capacidades": get_almacen_capacidades(),
                                },
                            )

                movimiento = form.save(commit=False)
                movimiento.save()
                for detalle_form in formset:
                    if (
                        detalle_form.cleaned_data.get("lote")
                        and detalle_form.cleaned_data.get("cantidad")
                        and not detalle_form.cleaned_data.get("DELETE")
                    ):
                        detalle = detalle_form.save(commit=False)
                        detalle.movimiento = movimiento
                        detalle.save()

                        lote = detalle.lote
                        cantidad = detalle.cantidad

                        if tipo == "entrada":
                            inv, created = Inventario.objects.get_or_create(
                                almacen=almacen, lote=lote, defaults={"cantidad": 0}
                            )
                            inv.cantidad += cantidad
                            inv.save()
                        elif tipo == "salida":
                            inv, created = Inventario.objects.get_or_create(
                                almacen=almacen, lote=lote, defaults={"cantidad": 0}
                            )
                            inv.cantidad = max(0, inv.cantidad - cantidad)
                            inv.save()
                        elif tipo == "transferencia":
                            almacen_destino = form.cleaned_data.get("almacen_destino")
                            if almacen_destino:
                                inv_salida, created = Inventario.objects.get_or_create(
                                    almacen=almacen, lote=lote, defaults={"cantidad": 0}
                                )
                                inv_salida.cantidad = max(
                                    0, inv_salida.cantidad - cantidad
                                )
                                inv_salida.save()

                                inv_entrada, created = Inventario.objects.get_or_create(
                                    almacen=almacen_destino,
                                    lote=lote,
                                    defaults={"cantidad": 0},
                                )
                                inv_entrada.cantidad += cantidad
                                inv_entrada.save()

                messages.success(request, "Movimiento creado exitosamente.")
                return redirect("inventario:movimiento_list")
        else:
            formset_errors = formset.errors
    else:
        form = MovimientoForm()
        formset = DetalleFormSet(queryset=DetalleMovimiento.objects.none())
        formset_errors = None

    return render(
        request,
        "inventario/movimiento_form.html",
        {
            "form": form,
            "detalle_formset": formset,
            "movimiento": None,
            "formset_errors": formset_errors,
            "almacen_capacidades": get_almacen_capacidades(),
        },
    )


@login_required
def movimiento_delete(request, id):
    movimiento = get_object_or_404(Movimiento, id=id)
    if request.method == "POST":
        tipo = movimiento.tipo
        almacen = movimiento.almacen
        almacen_destino = movimiento.almacen_destino
        for detalle in movimiento.detallemovimiento_set.all():
            lote = detalle.lote
            cantidad = detalle.cantidad
            if tipo == "entrada":
                inv = Inventario.objects.filter(almacen=almacen, lote=lote).first()
                if inv:
                    inv.cantidad = max(0, inv.cantidad - cantidad)
                    inv.save()
            elif tipo == "salida":
                inv, created = Inventario.objects.get_or_create(
                    almacen=almacen, lote=lote, defaults={"cantidad": 0}
                )
                inv.cantidad += cantidad
                inv.save()
            elif tipo == "transferencia" and almacen_destino:
                inv_salida = Inventario.objects.filter(
                    almacen=almacen, lote=lote
                ).first()
                if inv_salida:
                    inv_salida.cantidad += cantidad
                    inv_salida.save()

                inv_entrada = Inventario.objects.filter(
                    almacen=almacen_destino, lote=lote
                ).first()
                if inv_entrada:
                    inv_entrada.cantidad = max(0, inv_entrada.cantidad - cantidad)
                    inv_entrada.save()
        movimiento.delete()
    return redirect("inventario:movimiento_list")
