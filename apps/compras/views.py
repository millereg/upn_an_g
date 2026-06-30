from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from django.utils import timezone
from django.db import models
from .models import Proveedor, Compra, DetalleCompra
from .forms import ProveedorForm, CompraForm, DetalleCompraForm
from apps.inventario.models import Movimiento, DetalleMovimiento, Inventario
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
def proveedor_list(request):
    proveedores = (
        Proveedor.objects.select_related("ciudad", "provincia", "departamento", "pais")
        .all()
        .order_by("nombre")
    )
    q = request.GET.get('q', '').strip()
    if q:
        proveedores = proveedores.filter(nombre__icontains=q)
    return render(request, "compras/proveedor_list.html", {"proveedores": proveedores, "q": q})


@login_required
def proveedor_create(request):
    if request.method == "POST":
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor creado exitosamente.")
            return redirect("compras:proveedor_list")
    else:
        form = ProveedorForm()
    return render(
        request, "compras/proveedor_form.html", {"form": form, "proveedor": None}
    )


@login_required
def proveedor_update(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == "POST":
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, "Proveedor actualizado exitosamente.")
            return redirect("compras:proveedor_list")
    else:
        form = ProveedorForm(instance=proveedor)
    return render(
        request, "compras/proveedor_form.html", {"form": form, "proveedor": proveedor}
    )


@login_required
def proveedor_delete(request, id):
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == "POST":
        proveedor.delete()
    return redirect("compras:proveedor_list")


@login_required
def compra_list(request):
    compras = (
        Compra.objects.select_related("proveedor", "almacen")
        .all()
        .order_by("-fecha_creacion")
    )
    q = request.GET.get('q', '').strip()
    if q:
        compras = compras.filter(numero_documento__icontains=q)
    return render(request, "compras/compra_list.html", {"compras": compras, "q": q})


@login_required
def compra_create(request):
    DetalleFormSet = inlineformset_factory(
        Compra, DetalleCompra, form=DetalleCompraForm, extra=1, can_delete=True
    )
    if request.method == "POST":
        form = CompraForm(request.POST)
        formset = DetalleFormSet(request.POST)
        if form.is_valid():
            if formset.is_valid():
                compra = form.save()
                almacen = compra.almacen

                total_cantidad = 0
                for detalle_form in formset:
                    if (
                        detalle_form.cleaned_data.get("cantidad")
                        and not detalle_form.cleaned_data.get("DELETE")
                    ):
                        total_cantidad += detalle_form.cleaned_data.get("cantidad", 0)

                puede_agregar, stock_actual, capacidad = verificar_capacidad(almacen, total_cantidad)
                if not puede_agregar:
                    messages.error(
                        request,
                        f"Almacén '{almacen.nombre}' sin capacidad suficiente. Stock actual: {stock_actual}, Capacidad: {capacidad}, Intentando agregar: {total_cantidad}"
                    )
                    return render(
                        request,
                        "compras/compra_form.html",
                        {"form": form, "detalle_formset": formset, "compra": None, "almacen_capacidades": get_almacen_capacidades()},
                    )

                movimiento = Movimiento.objects.create(
                    tipo="entrada",
                    almacen=compra.almacen,
                    referencia=compra.numero_documento,
                    fecha=timezone.now(),
                    estado="confirmado",
                )

                for detalle_form in formset:
                    if (
                        detalle_form.cleaned_data.get("producto")
                        and detalle_form.cleaned_data.get("cantidad")
                        and not detalle_form.cleaned_data.get("DELETE")
                    ):
                        detalle = detalle_form.save(commit=False)
                        detalle.compra = compra
                        detalle.save()

                        lote = detalle.lote
                        cantidad = detalle.cantidad

                        inv, created = Inventario.objects.get_or_create(
                            almacen=compra.almacen, lote=lote, defaults={"cantidad": 0}
                        )
                        inv.cantidad += cantidad
                        inv.save()

                        DetalleMovimiento.objects.create(
                            movimiento=movimiento, lote=lote, cantidad=cantidad
                        )

                messages.success(request, "Compra creada exitosamente.")
                return redirect("compras:compra_list")
    else:
        form = CompraForm()
        formset = DetalleFormSet(queryset=DetalleCompra.objects.none())
    return render(
        request,
        "compras/compra_form.html",
        {"form": form, "detalle_formset": formset, "compra": None, "almacen_capacidades": get_almacen_capacidades()},
    )


@login_required
def compra_update(request, id):
    compra = get_object_or_404(Compra, id=id)
    DetalleFormSet = inlineformset_factory(
        Compra, DetalleCompra, form=DetalleCompraForm, extra=0, can_delete=True
    )
    if request.method == "POST":
        form = CompraForm(request.POST, instance=compra)
        formset = DetalleFormSet(request.POST, instance=compra)
        if form.is_valid():
            if formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, "Compra actualizada exitosamente.")
                return redirect("compras:compra_list")
    else:
        form = CompraForm(instance=compra)
        formset = DetalleFormSet(instance=compra)
    return render(
        request,
        "compras/compra_form.html",
        {"form": form, "detalle_formset": formset, "compra": compra},
    )


@login_required
def compra_delete(request, id):
    compra = get_object_or_404(Compra, id=id)
    if request.method == "POST":
        Movimiento.objects.filter(referencia=compra.numero_documento, tipo='entrada').delete()

        for detalle in compra.detallecompra_set.all():
            lote = detalle.lote
            cantidad = detalle.cantidad
            inv = Inventario.objects.filter(almacen=compra.almacen, lote=lote).first()
            if inv:
                inv.cantidad = max(0, inv.cantidad - cantidad)
                inv.save()

        compra.delete()
    return redirect("compras:compra_list")
