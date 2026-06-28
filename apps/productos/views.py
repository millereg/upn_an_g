from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria, Producto, Lote
from .forms import CategoriaForm, LoteForm, ProductoForm


@login_required
def categoria_list(request):
    categorias = Categoria.objects.all().order_by("nombre")
    form = CategoriaForm()
    return render(
        request,
        "productos/categoria_list.html",
        {"categorias": categorias, "form": form},
    )


@login_required
def categoria_create(request):
    if request.method == "POST":
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría creada exitosamente.")
        else:
            messages.error(request, "Error al crear la categoría.")
    return redirect("productos:categoria_list")


@login_required
def categoria_update(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, "Categoría actualizada exitosamente.")
        else:
            messages.error(request, "Error al actualizar la categoría.")
    return redirect("productos:categoria_list")


@login_required
def categoria_delete(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        categoria.delete()
    return redirect("productos:categoria_list")


@login_required
def producto_list(request):
    productos = Producto.objects.select_related("categoria").all().order_by("nombre")
    form = ProductoForm()
    return render(
        request, "productos/producto_list.html", {"productos": productos, "form": form}
    )


@login_required
def producto_delete(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        producto.delete()
    return redirect("productos:producto_list")


@login_required
def producto_create(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto creado exitosamente.")
        else:
            messages.error(request, "Error al crear el producto.")
    return redirect("productos:producto_list")


@login_required
def producto_update(request, id):
    producto = get_object_or_404(Producto, id=id)
    if request.method == "POST":
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, "Producto actualizado exitosamente.")
        else:
            messages.error(request, "Error al actualizar el producto.")
    return redirect("productos:producto_list")


@login_required
def lote_list(request):
    lotes = (
        Lote.objects.select_related("producto", "proveedor")
        .all()
        .order_by("numero_lote")
    )
    form = LoteForm()
    return render(request, "productos/lote_list.html", {"lotes": lotes, "form": form})


@login_required
def lote_delete(request, id):
    lote = get_object_or_404(Lote, id=id)
    if request.method == "POST":
        lote.delete()
    return redirect("productos:lote_list")


@login_required
def lote_create(request):
    if request.method == "POST":
        form = LoteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Lote creado exitosamente.")
        else:
            messages.error(request, "Error al crear el lote.")
    return redirect("productos:lote_list")


@login_required
def lote_update(request, id):
    lote = get_object_or_404(Lote, id=id)
    if request.method == "POST":
        form = LoteForm(request.POST, instance=lote)
        if form.is_valid():
            form.save()
            messages.success(request, "Lote actualizado exitosamente.")
        else:
            messages.error(request, "Error al actualizar el lote.")
    return redirect("productos:lote_list")
