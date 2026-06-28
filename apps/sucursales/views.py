from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Sucursal, Almacen
from .forms import AlmacenForm, SucursalForm


@login_required
def sucursal_list(request):
    sucursales = Sucursal.objects.select_related('ciudad', 'provincia', 'departamento', 'pais').all().order_by('nombre')
    return render(request, 'sucursales/sucursal_list.html', {'sucursales': sucursales})


@login_required
def sucursal_create(request):
    if request.method == 'POST':
        form = SucursalForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucursal creada exitosamente.')
            return redirect('sucursales:sucursal_list')
    else:
        form = SucursalForm()
    return render(request, 'sucursales/sucursal_form.html', {'form': form, 'sucursal': None})


@login_required
def sucursal_update(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    if request.method == 'POST':
        form = SucursalForm(request.POST, instance=sucursal)
        if form.is_valid():
            form.save()
            messages.success(request, 'Sucursal actualizada exitosamente.')
            return redirect('sucursales:sucursal_list')
    else:
        form = SucursalForm(instance=sucursal)
    return render(request, 'sucursales/sucursal_form.html', {'form': form, 'sucursal': sucursal})


@login_required
def sucursal_delete(request, id):
    sucursal = get_object_or_404(Sucursal, id=id)
    if request.method == 'POST':
        sucursal.delete()
    return redirect('sucursales:sucursal_list')


@login_required
def almacen_list(request):
    almacenes = Almacen.objects.select_related('sucursal').all().order_by('nombre')
    sucursales = Sucursal.objects.filter(estado='activo').order_by('nombre')
    form = AlmacenForm()
    return render(request, 'sucursales/almacen_list.html', {'almacenes': almacenes, 'sucursales': sucursales, 'form': form})


@login_required
def almacen_create(request):
    if request.method == 'POST':
        form = AlmacenForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Almacén creado exitosamente.')
        else:
            messages.error(request, 'Error al crear el almacén.')
    return redirect('sucursales:almacen_list')


@login_required
def almacen_update(request, id):
    almacen = get_object_or_404(Almacen, id=id)
    if request.method == 'POST':
        form = AlmacenForm(request.POST, instance=almacen)
        if form.is_valid():
            form.save()
            messages.success(request, 'Almacén actualizado exitosamente.')
        else:
            messages.error(request, 'Error al actualizar el almacén.')
    return redirect('sucursales:almacen_list')


@login_required
def almacen_delete(request, id):
    almacen = get_object_or_404(Almacen, id=id)
    if request.method == 'POST':
        almacen.delete()
    return redirect('sucursales:almacen_list')
