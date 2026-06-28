from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Perfil
from .forms import UsuarioForm, UsuarioEditForm, PerfilForm


@login_required
def usuario_list(request):
    usuarios = User.objects.all().order_by("username")
    return render(request, "usuarios/usuario_list.html", {"usuarios": usuarios})


@login_required
def usuario_create(request):
    if request.method == "POST":
        user_form = UsuarioForm(request.POST)
        perfil_form = PerfilForm(request.POST, request.FILES)
        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            return redirect("usuarios:usuario_list")
    else:
        user_form = UsuarioForm()
        perfil_form = PerfilForm()
    return render(
        request,
        "usuarios/usuario_form.html",
        {
            "user_form": user_form,
            "perfil_form": perfil_form,
        },
    )


@login_required
def usuario_update(request, id):
    usuario_edit = get_object_or_404(User, id=id)
    perfil, _ = Perfil.objects.get_or_create(user=usuario_edit)
    if request.method == "POST":
        user_form = UsuarioEditForm(request.POST, instance=usuario_edit)
        perfil_form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()
            return redirect("usuarios:usuario_list")
    else:
        user_form = UsuarioEditForm(instance=usuario_edit)
        perfil_form = PerfilForm(instance=perfil)
    return render(
        request,
        "usuarios/usuario_form.html",
        {
            "user_form": user_form,
            "perfil_form": perfil_form,
            "usuario_edit": usuario_edit,
        },
    )


@login_required
def usuario_delete(request, id):
    user = get_object_or_404(User, id=id)
    if request.method == "POST":
        user.delete()
    return redirect("usuarios:usuario_list")
