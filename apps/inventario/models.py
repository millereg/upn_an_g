from django.db import models
from django.conf import settings

# Create your models here.

class Inventario(models.Model):
    almacen = models.ForeignKey('sucursales.Almacen', on_delete=models.PROTECT)
    lote = models.ForeignKey('productos.Lote', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    
    class Meta:
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"
    
class Movimiento(models.Model):
    TIPO = [
        ('entrada', 'Entrada'),
        ('salida', 'Salida'),
        ('ajuste', 'Ajuste'),
        ('transferencia', 'Transferencia'),
    ]

    ESTADO = [
        ('pendiente', 'Pendiente'),
        ('confirmado', 'Confirmado'),
        ('anulado', 'Anulado'),
    ]

    tipo = models.CharField(max_length=15, choices=TIPO)
    almacen = models.ForeignKey('sucursales.Almacen', on_delete=models.PROTECT, related_name='movimientos_origen')
    almacen_destino = models.ForeignKey('sucursales.Almacen', on_delete=models.PROTECT, related_name='movimientos_destino', null=True, blank=True)
    referencia = models.CharField(max_length=100)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=15, choices=ESTADO, default='pendiente')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_creados')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='movimientos_actualizados')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Movimiento"
        verbose_name_plural = "Movimientos"
        
class DetalleMovimiento(models.Model):
    movimiento = models.ForeignKey(Movimiento, on_delete=models.CASCADE)
    lote = models.ForeignKey('productos.Lote', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    
    class Meta:
        verbose_name = "Detalle de Movimiento"
        verbose_name_plural = "Detalles de Movimientos"