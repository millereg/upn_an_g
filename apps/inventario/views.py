from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from .models import Inventario, Movimiento, DetalleMovimiento
from .forms import MovimientoForm, DetalleMovimientoForm


@login_required
def inventario_list(request):
    inventario = (
        Inventario.objects.select_related("almacen", "lote__producto")
        .all()
        .order_by("-id")
    )
    return render(
        request, "inventario/inventario_list.html", {"inventario": inventario}
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
    return render(
        request, "inventario/movimiento_list.html", {"movimientos": movimientos}
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
