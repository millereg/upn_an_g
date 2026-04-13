from django.contrib import admin

from .models import Modulo, PermisoModulo, TipoPermiso


class SubmoduloInline(admin.TabularInline):
    model   = Modulo
    fk_name = 'padre'
    extra   = 0
    fields  = ('nombre', 'codigo', 'url', 'icono', 'orden', 'estado')


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display        = ('orden', 'nombre', 'codigo', 'url', 'estado', 'padre')
    list_display_links  = ('nombre',)
    list_editable       = ('orden', 'estado')
    list_filter         = ('estado', 'padre')
    search_fields       = ('nombre', 'codigo')
    prepopulated_fields = {'codigo': ('nombre',)}
    inlines             = [SubmoduloInline]


@admin.register(TipoPermiso)
class TipoPermisoAdmin(admin.ModelAdmin):
    list_display       = ('orden', 'nombre', 'codigo')
    list_display_links = ('nombre',)
    list_editable      = ('orden',)
    search_fields      = ('nombre', 'codigo')


@admin.register(PermisoModulo)
class PermisoModuloAdmin(admin.ModelAdmin):
    list_display  = ('grupo', 'modulo', 'permiso')
    list_filter   = ('grupo', 'modulo', 'permiso')
    search_fields = ('grupo__name', 'modulo__nombre', 'permiso__nombre')

