from django.db import models
from django.conf import settings

# Create your models here.

class Venta(models.Model):
    TIPO_DOC = [
        ('Factura', 'Factura'),
        ('Boleta', 'Boleta'),
        ('Nota de pedido', 'Nota de pedido'),
        ('Recibo', 'Recibo'),
    ]

    ESTADO = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ]

    sucursal = models.ForeignKey('sucursales.Sucursal', on_delete=models.PROTECT)
    almacen = models.ForeignKey('sucursales.Almacen', on_delete=models.PROTECT, null=True, blank=True)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOC)
    numero_documento = models.CharField(max_length=50)
    estado = models.CharField(max_length=15, choices=ESTADO, default='pendiente')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_creadas')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='ventas_actualizadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    lote = models.ForeignKey('productos.Lote', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"