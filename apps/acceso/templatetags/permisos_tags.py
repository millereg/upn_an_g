from django import template
from collections import defaultdict
from apps.acceso.models import PermisoModulo

register = template.Library()


@register.simple_tag
def has_perm(user, module_codigo, perm_codigo):
    if not user or not user.is_authenticated:
        return False
    return PermisoModulo.objects.filter(
        grupo__in=user.groups.all(),
        modulo__codigo=module_codigo,
        permiso__codigo=perm_codigo
    ).exists()


@register.simple_tag
def get_modulos_por_grupo(user):
    if not user or not user.is_authenticated:
        return {}

    grupos = user.groups.all()
    if not grupos.exists():
        return {}

    permisos = PermisoModulo.objects.filter(
        grupo__in=grupos,
        permiso__codigo='ver'
    ).select_related('modulo', 'permiso')

    modulos_dict = defaultdict(list)
    seen = set()

    for p in permisos:
        m = p.modulo
        if m.estado != 'A' or m.id in seen:
            continue
        seen.add(m.id)
        grupo_menu = m.grupo_menu or 'Sin Grupo'
        modulos_dict[grupo_menu].append(m)

    orden_grupos = ['Inicio', 'Seguridad', 'Inventario', 'Operaciones', 'Configuración']
    result = {}
    for g in orden_grupos:
        if g in modulos_dict:
            result[g] = sorted(modulos_dict[g], key=lambda x: x.orden)
    for g, mods in modulos_dict.items():
        if g not in result:
            result[g] = sorted(mods, key=lambda x: x.orden)

    return result
