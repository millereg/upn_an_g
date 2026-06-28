from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from .forms import LoginForm, GrupoForm
from .models import Modulo, PermisoModulo


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                if not user.is_active:
                    form.add_error(None, "Usuario inactivo. Contacte al administrador.")
                else:
                    login(request, user)
                    return redirect("dashboard:index")
            else:
                form.add_error(None, "Credenciales inválidas")
    return render(request, "acceso/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def modulo_list(request):
    modulos = Modulo.objects.all().order_by('grupo_menu', 'orden')
    return render(request, 'acceso/modulo_list.html', {'modulos': modulos})


@login_required
def modulo_delete(request, id):
    modulo = get_object_or_404(Modulo, id=id)
    if request.method == 'POST':
        modulo.delete()
    return redirect('acceso:modulo_list')


@login_required
def permiso_list(request):
    permisos = PermisoModulo.objects.select_related('grupo', 'modulo', 'permiso').all()
    return render(request, 'acceso/permission_list.html', {'permisos': permisos})


@login_required
def permiso_delete(request, id):
    permiso = get_object_or_404(PermisoModulo, id=id)
    if request.method == 'POST':
        permiso.delete()
    return redirect('acceso:permiso_list')


@login_required
def grupo_list(request):
    grupos = Group.objects.all().order_by('name')
    form = GrupoForm()
    return render(request, 'acceso/grupo_list.html', {'grupos': grupos, 'form': form})


@login_required
def grupo_create(request):
    if request.method == 'POST':
        form = GrupoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo creado exitosamente.')
        else:
            messages.error(request, 'Error al crear el grupo.')
    return redirect('acceso:grupo_list')


@login_required
def grupo_update(request, id):
    grupo = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        form = GrupoForm(request.POST, instance=grupo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Grupo actualizado exitosamente.')
        else:
            messages.error(request, 'Error al actualizar el grupo.')
    return redirect('acceso:grupo_list')


@login_required
def grupo_delete(request, id):
    grupo = get_object_or_404(Group, id=id)
    if request.method == 'POST':
        grupo.delete()
    return redirect('acceso:grupo_list')