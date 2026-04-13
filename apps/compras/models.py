from django.db import models
from django.conf import settings

# Create your models here.

class Proveedor(models.Model):
    TIPO_DOC = [
        ('dni', 'DNI'),
        ('pasaporte', 'Pasaporte'),
        ('ruc', 'RUC'),
    ]

    ESTADO = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=50)
    tipo_documento = models.CharField(max_length=15, choices=TIPO_DOC, default='dni')
    documento = models.CharField(max_length=25)
    pais = models.ForeignKey('ubicacion.Pais', on_delete=models.PROTECT)
    departamento = models.ForeignKey('ubicacion.Departamento', on_delete=models.PROTECT)
    provincia = models.ForeignKey('ubicacion.Provincia', on_delete=models.PROTECT)
    ciudad = models.ForeignKey('ubicacion.Ciudad', on_delete=models.PROTECT)
    direccion = models.CharField(max_length=85)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    correo = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, choices=ESTADO, default='activo')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='proveedores_creados')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='proveedores_actualizados')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.nombre

class Compra(models.Model):
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

    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    almacen = models.ForeignKey('sucursales.Almacen', on_delete=models.PROTECT)
    tipo_documento = models.CharField(max_length=20, choices=TIPO_DOC)
    numero_documento = models.CharField(max_length=50)
    estado = models.CharField(max_length=15, choices=ESTADO, default='pendiente')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_creadas')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='compras_actualizadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Compra"
        verbose_name_plural = "Compras"


class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey('productos.Producto', on_delete=models.PROTECT)
    lote = models.ForeignKey('productos.Lote', on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = "Detalle de Compra"
        verbose_name_plural = "Detalles de Compras"