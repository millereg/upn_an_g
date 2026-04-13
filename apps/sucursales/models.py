from django.db import models
from django.conf import settings

# Create your models here.

class Sucursal(models.Model):
    ESTADO = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=50)
    codigo = models.CharField(max_length=25)
    pais = models.ForeignKey('ubicacion.Pais', on_delete=models.PROTECT)
    departamento = models.ForeignKey('ubicacion.Departamento', on_delete=models.PROTECT)
    provincia = models.ForeignKey('ubicacion.Provincia', on_delete=models.PROTECT)
    ciudad = models.ForeignKey('ubicacion.Ciudad', on_delete=models.PROTECT)
    direccion = models.CharField(max_length=85)
    referencia = models.CharField(max_length=50)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    celular = models.CharField(max_length=20, blank=True, null=True)
    correo = models.CharField(max_length=50)
    estado = models.CharField(max_length=10, choices=ESTADO, default='activo')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sucursales_creadas')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sucursales_actualizadas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

    def __str__(self):
        return self.nombre

class Almacen(models.Model):
    TIPO = [
        ('principal', 'Principal'),
        ('secundario', 'Secundario'),
        ('transito', 'Tránsito'),
        ('cuarentena', 'Cuarentena'),
    ]

    ESTADO = [
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    ]

    sucursal = models.ForeignKey(Sucursal, on_delete=models.PROTECT)
    nombre = models.CharField(max_length=50)
    tipo = models.CharField(max_length=15, choices=TIPO, default='principal')
    estado = models.CharField(max_length=10, choices=ESTADO, default='activo')
    creado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='almacenes_creados')
    actualizado_por = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='almacenes_actualizados')
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True, null=True)
    
    class Meta:
        verbose_name = "Almacén"
        verbose_name_plural = "Almacenes"

    def __str__(self):
        return self.nombre