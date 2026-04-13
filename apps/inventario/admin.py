from django.contrib import admin
from .models import Inventario, Movimiento, DetalleMovimiento

# Register your models here.
class DetalleMovimientoInline(admin.TabularInline):
    model = DetalleMovimiento
    extra = 1

class MovimientoAdmin(admin.ModelAdmin):
    inlines = [DetalleMovimientoInline]

admin.site.register(Inventario)
admin.site.register(Movimiento, MovimientoAdmin)