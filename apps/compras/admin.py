from django.contrib import admin
from .models import Proveedor, Compra, DetalleCompra

# Register your models here.
class DetalleCompraInline(admin.TabularInline):
    model = DetalleCompra
    extra = 1

class CompraAdmin(admin.ModelAdmin):
    inlines = [DetalleCompraInline]

admin.site.register(Proveedor)
admin.site.register(Compra, CompraAdmin)