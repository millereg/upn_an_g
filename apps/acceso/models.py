from django.contrib.auth.models import Group
from django.db import models


class Modulo(models.Model):
    ACTIVO   = 'A'
    INACTIVO = 'I'
    ESTADO_CHOICES = [
        (ACTIVO,   'Activo'),
        (INACTIVO, 'Inactivo'),
    ]

    nombre  = models.CharField(max_length=100, unique=True)
    codigo  = models.SlugField(max_length=100, unique=True,
                               help_text="Identificador único sin espacios, p.ej. 'ventas'")
    icono   = models.CharField(max_length=80, blank=True,
                               help_text="Clase CSS del ícono, p.ej. 'bi bi-cart'")
    url     = models.CharField(max_length=200, blank=True,
                               help_text="Nombre de URL o ruta, p.ej. 'ventas:lista'")
    grupo_menu = models.CharField(max_length=80, blank=True,
                                help_text="Título de sección en el sidebar, p.ej. 'Ventas', 'Configuración'")
    orden   = models.PositiveSmallIntegerField(default=0,
                                              help_text="Orden en el menú")
    padre   = models.ForeignKey('self', null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='submodulos',
                                help_text="Módulo padre para submenús")
    estado  = models.CharField(max_length=1, choices=ESTADO_CHOICES,
                               default=ACTIVO)

    class Meta:
        verbose_name        = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering            = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class TipoPermiso(models.Model):
    nombre  = models.CharField(max_length=80, unique=True,
                               help_text="Nombre legible, p.ej. 'Ver Reportes'")
    codigo  = models.SlugField(max_length=80, unique=True,
                               help_text="Clave interna, p.ej. 'ver_reportes'")
    orden   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name        = 'Tipo de permiso'
        verbose_name_plural = 'Tipos de permiso'
        ordering            = ['orden', 'nombre']

    def __str__(self):
        return self.nombre


class PermisoModulo(models.Model):
    grupo   = models.ForeignKey(Group, on_delete=models.CASCADE,
                                related_name='permisos_modulos')
    modulo  = models.ForeignKey(Modulo, on_delete=models.CASCADE,
                                related_name='permisos_grupos')
    permiso = models.ForeignKey(TipoPermiso, on_delete=models.CASCADE,
                                related_name='asignaciones')

    class Meta:
        verbose_name        = 'Permiso de módulo'
        verbose_name_plural = 'Permisos de módulos'
        unique_together     = ('grupo', 'modulo', 'permiso')

    def __str__(self):
        return f"{self.grupo} | {self.modulo} | {self.permiso}"
