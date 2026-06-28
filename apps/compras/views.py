from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Proveedor, Compra, DetalleCompra
from .forms import ProveedorForm, CompraForm, DetalleCompraForm
from apps.inventario.models import Movimiento, DetalleMovimiento, Inventario


@login_required
def proveedor_list(request):
    proveedores = (
        Proveedor.objects.select_related("ciudad", "provincia", "departamento", "pais")
        .all()
        .order_by("nombre")
    )
    return render(request, "compras/proveedor_list.html", {"proveedores": proveedores})


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
    return render(request, "compras/compra_list.html", {"compras": compras})


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
        {"form": form, "detalle_formset": formset, "compra": None},
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
