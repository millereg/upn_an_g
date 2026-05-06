from django.shortcuts import render, redirect, get_object_or_404
from .models import PermisoModulo
from .forms import PermisoModuloForm


def permission_list(request):
    permissions = PermisoModulo.objects.all()

    return render(
        request,
        'acceso/permission_list.html',
        {'permissions': permissions},
    )

def permission_create(request):
    if request.method == 'POST':
        form = PermisoModuloForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('acceso:permission_list')

    else:
        form = PermisoModuloForm()

    return render(
        request,
        'acceso/permission_form.html',
        {'form': form},
    )

def permission_update(request, id):
    permission = get_object_or_404(PermisoModulo, id=id)

    if request.method == 'POST':
        form = PermisoModuloForm(request.POST, instance=permission)

        if form.is_valid():
            form.save()
            return redirect('acceso:permission_list')

    else:
        form = PermisoModuloForm(instance=permission)

    return render(
        request,
        'acceso/permission_form.html',
        {'form': form}
    )


def permission_delete(request, id):
    permmission = get_object_or_404(PermisoModulo, id=id)
    if request.method == 'POST':
        permmission.delete()
        return redirect('acceso:permission_list')

    return render(
        request,
        'acceso/permission_confirm_delete.html',
        {'permission': permmission},
    )