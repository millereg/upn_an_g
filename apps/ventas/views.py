from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.forms import inlineformset_factory
from django.utils import timezone
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaForm
from apps.inventario.models import Movimiento, DetalleMovimiento, Inventario


@login_required
def venta_list(request):
    ventas = Venta.objects.select_related('sucursal').all().order_by('-fecha_creacion')
    return render(request, 'ventas/venta_list.html', {'ventas': ventas})


@login_required
def venta_create(request):
    DetalleFormSet = inlineformset_factory(
        Venta, DetalleVenta,
        form=DetalleVentaForm,
        extra=1,
        can_delete=True
    )
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = DetalleFormSet(request.POST)
        if form.is_valid():
            if formset.is_valid():
                venta = form.save()

                movimiento = Movimiento.objects.create(
                    tipo='salida',
                    almacen=venta.almacen,
                    referencia=venta.numero_documento,
                    fecha=timezone.now(),
                    estado='confirmado'
                )

                for detalle_form in formset:
                    if detalle_form.cleaned_data.get('lote') and detalle_form.cleaned_data.get('cantidad') and not detalle_form.cleaned_data.get('DELETE'):
                        detalle = detalle_form.save(commit=False)
                        detalle.venta = venta
                        detalle.save()

                        lote = detalle.lote
                        cantidad = detalle.cantidad

                        inv = Inventario.objects.filter(almacen=venta.almacen, lote=lote).first()
                        if inv:
                            inv.cantidad = max(0, inv.cantidad - cantidad)
                            inv.save()

                        DetalleMovimiento.objects.create(
                            movimiento=movimiento,
                            lote=lote,
                            cantidad=cantidad
                        )

                messages.success(request, 'Venta creada exitosamente.')
                return redirect('ventas:venta_list')
    else:
        form = VentaForm()
        formset = DetalleFormSet(queryset=DetalleVenta.objects.none())
    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'detalle_formset': formset,
        'venta': None
    })


@login_required
def venta_update(request, id):
    venta = get_object_or_404(Venta, id=id)
    DetalleFormSet = inlineformset_factory(
        Venta, DetalleVenta,
        form=DetalleVentaForm,
        extra=0,
        can_delete=True
    )
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = DetalleFormSet(request.POST, instance=venta)
        if form.is_valid():
            if formset.is_valid():
                form.save()
                formset.save()
                messages.success(request, 'Venta actualizada exitosamente.')
                return redirect('ventas:venta_list')
    else:
        form = VentaForm(instance=venta)
        formset = DetalleFormSet(instance=venta)
    return render(request, 'ventas/venta_form.html', {
        'form': form,
        'detalle_formset': formset,
        'venta': venta
    })


@login_required
def venta_delete(request, id):
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        Movimiento.objects.filter(referencia=venta.numero_documento, tipo='salida').delete()

        for detalle in venta.detalleventa_set.all():
            lote = detalle.lote
            cantidad = detalle.cantidad
            inv = Inventario.objects.filter(almacen=venta.almacen, lote=lote).first()
            if inv:
                inv.cantidad += cantidad
                inv.save()

        venta.delete()
    return redirect('ventas:venta_list')