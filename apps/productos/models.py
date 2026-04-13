from django.db import models
from django.conf import settings

# Create your models here.

class Categoria(models.Model):
    ESTADO = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, choices=ESTADO, default='activo')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='categorias_creadas')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='categorias_actualizadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    ESTADO = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    referencia = models.CharField(max_length=50)
    nombre = models.CharField(max_length=90)
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    codigo_barra = models.CharField(max_length=50, blank=True, null=True)
    requiere_receta = models.BooleanField(default=False)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=10, choices=ESTADO, default='activo')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_creados')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='productos_actualizados')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre

class Lote(models.Model):
    ESTADO = [
        ('activo', 'Activo'),
        ('vencido', 'Vencido'),
        ('bloqueado', 'Bloqueado'),
        ('cuarentena', 'Cuarentena'),
    ]

    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    proveedor = models.ForeignKey('compras.Proveedor', on_delete=models.PROTECT)
    numero_lote = models.CharField(max_length=50)
    fecha_vencimiento = models.DateField()
    registro_sanitario = models.CharField(max_length=100)
    estado = models.CharField(max_length=15, choices=ESTADO, default='activo')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='lotes_creados')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='lotes_actualizados')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Lote"
        verbose_name_plural = "Lotes"

    def __str__(self):
        return self.numero_lote