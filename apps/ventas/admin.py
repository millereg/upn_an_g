from django.contrib import admin
from .models import Venta, DetalleVenta

# Register your models here.
class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

class VentaAdmin(admin.ModelAdmin):
    inlines = [DetalleVentaInline]

admin.site.register(Venta, VentaAdmin)
