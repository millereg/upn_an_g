from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.db import transaction

from apps.acceso.models import Modulo, TipoPermiso, PermisoModulo


MODULOS = [
    # Inicio
    (1, "Dashboard", "dashboard", "fas fa-fw fa-tachometer-alt", "dashboard:index", "Inicio", 1, None),
    # Seguridad
    (2, "Acceso", "acceso", "fas fa-fw fa-lock", "", "Seguridad", 10, None),
    (3, "Usuarios", "usuarios", "fas fa-fw fa-users", "usuarios:usuario_list", "Seguridad", 11, None),
    (4, "Grupos", "grupos", "fas fa-fw fa-users-cog", "acceso:grupo_list", "Seguridad", 12, None),
    (5, "Módulos", "modulos", "fas fa-fw fa-sitemap", "acceso:modulo_list", "Seguridad", 13, None),
    (6, "Permisos", "permisos", "fas fa-fw fa-key", "acceso:permiso_list", "Seguridad", 14, None),
    # Inventario
    (7, "Inventario", "inventario", "fas fa-fw fa-boxes", "", "Inventario", 20, None),
    (8, "Productos", "productos", "fas fa-fw fa-box", "productos:producto_list", "Inventario", 21, None),
    (9, "Categorías", "categorias", "fas fa-fw fa-tags", "productos:categoria_list", "Inventario", 22, None),
    (10, "Lotes", "lotes", "fas fa-fw fa-layer-group", "productos:lote_list", "Inventario", 23, None),
    (11, "Stock", "stock", "fas fa-fw fa-cubes", "inventario:inventario_list", "Inventario", 24, None),
    (12, "Movimientos", "movimientos", "fas fa-fw fa-exchange-alt", "inventario:movimiento_list", "Inventario", 25, None),
    (13, "Almacenes", "almacenes", "fas fa-fw fa-warehouse", "sucursales:almacen_list", "Inventario", 26, None),
    (14, "Sucursales", "sucursales", "fas fa-fw fa-store", "sucursales:sucursal_list", "Inventario", 27, None),
    # Operaciones
    (15, "Operaciones", "operaciones", "fas fa-fw fa-clipboard-list", "", "Operaciones", 30, None),
    (16, "Compras", "compras", "fas fa-fw fa-cart-plus", "compras:compra_list", "Operaciones", 31, None),
    (17, "Proveedores", "proveedores", "fas fa-fw fa-truck", "compras:proveedor_list", "Operaciones", 32, None),
    (18, "Ventas", "ventas", "fas fa-fw fa-file-invoice-dollar", "ventas:venta_list", "Operaciones", 33, None),
    # Reportes
    (24, "Reportes", "reportes", "fas fa-fw fa-chart-bar", "", "Reportes", 35, None),
    (25, "Punto de Reorden", "punto_reorden", "fas fa-fw fa-exclamation-circle", "reportes:reorder_point", "Reportes", 36, 24),
    (26, "Asignación Almacenes", "asignacion_almacenes", "fas fa-fw fa-warehouse", "reportes:asignacion_almacenes", "Reportes", 37, 24),
    (27, "Planificación Compras", "planificacion_compras", "fas fa-fw fa-shopping-cart", "reportes:planificacion_compras", "Reportes", 38, 24),
    (28, "Pronóstico Demanda", "pronostico", "fas fa-fw fa-chart-line", "reportes:forecasting", "Reportes", 39, 24),
    (29, "Redistribución", "redistribucion", "fas fa-fw fa-exchange-alt", "reportes:redistribucion", "Reportes", 40, 24),
    # Configuración
    (19, "Ubicación", "ubicacion", "fas fa-fw fa-globe", "", "Configuración", 40, None),
    (20, "Países", "paises", "fas fa-fw fa-flag", "ubicacion:pais_list", "Configuración", 41, None),
    (21, "Departamentos", "departamentos", "fas fa-fw fa-building", "ubicacion:departamento_list", "Configuración", 42, None),
    (22, "Provincias", "provincias", "fas fa-fw fa-map", "ubicacion:provincia_list", "Configuración", 43, None),
    (23, "Ciudades", "ciudades", "fas fa-fw fa-city", "ubicacion:ciudad_list", "Configuración", 44, None),
]

GRUPOS = [
    (1, "Administrador"),
    (2, "Vendedor"),
    (3, "Almacenero"),
    (4, "Desarrollador"),
]

PERMISOS_GRUPO = {
    1: ('ver', 'crear', 'editar', 'eliminar', 'ver_reportes', 'exportar', 'imprimir', 'aprobar', 'anular'),
    2: ('ver', 'crear', 'editar', 'exportar', 'imprimir'),
    3: ('ver', 'crear', 'editar', 'aprobar', 'anular'),
    4: ('ver', 'crear', 'editar', 'eliminar', 'ver_reportes', 'exportar', 'imprimir', 'aprobar', 'anular'),
}

GRUPOS_MODULOS = {
    1: ("dashboard", "usuarios", "inventario", "productos", "categorias", "lotes", "stock",
         "movimientos", "almacenes", "sucursales",
         "operaciones", "compras", "proveedores", "ventas",
         "ubicacion", "paises", "departamentos", "provincias", "ciudades",
         "reportes", "reorder_point", "asignacion_almacenes", "planificacion_compras", "forecasting", "redistribucion"),
    2: ("dashboard", "operaciones", "compras", "proveedores", "ventas", "productos", "categorias",
         "reportes", "planificacion_compras", "forecasting"),
    3: ("dashboard", "inventario", "productos", "categorias", "lotes", "stock",
         "movimientos", "almacenes", "sucursales",
         "operaciones", "compras", "proveedores",
         "reportes", "reorder_point", "asignacion_almacenes", "redistribucion"),
    4: None,
}


class Command(BaseCommand):
    help = "Puebla módulos, tipos de permiso y grupos (no borra datos existentes)"

    def handle(self, *args, **options):
        self.stdout.write("Iniciando seed de acceso...")

        with transaction.atomic():
            self._create_or_update_modulos()
            self._create_or_update_grupos()
            self._sync_permisos()

        self.stdout.write(self.style.SUCCESS("Seed de acceso completado."))

    def _create_or_update_modulos(self):
        PermisoModulo.objects.all().delete()
        Modulo.objects.all().delete()
        created = 0
        for data in MODULOS:
            Modulo.objects.create(
                id=data[0],
                nombre=data[1],
                codigo=data[2],
                icono=data[3],
                url=data[4],
                grupo_menu=data[5],
                orden=data[6],
                padre_id=data[7],
                estado='A',
            )
            created += 1
        self.stdout.write(f"  {created} módulos creados")

    def _create_or_update_grupos(self):
        Group.objects.all().delete()
        created = 0
        for gid, name in GRUPOS:
            Group.objects.create(id=gid, name=name)
            created += 1
        self.stdout.write(f"  {created} grupos creados")

    def _sync_permisos(self):
        permisos = {tp.codigo: tp for tp in TipoPermiso.objects.all()}

        for gid, perms_codigos in PERMISOS_GRUPO.items():
            grupo = Group.objects.get(id=gid)
            modulos_permitidos = GRUPOS_MODULOS.get(gid)

            for modulo in Modulo.objects.filter(estado="A"):
                if modulos_permitidos and modulo.codigo not in modulos_permitidos:
                    continue
                for perm_codigo in perms_codigos:
                    if perm_codigo not in permisos:
                        continue
                    PermisoModulo.objects.get_or_create(
                        grupo=grupo, modulo=modulo, permiso=permisos[perm_codigo]
                    )

        self.stdout.write("  Permisos sincronizados")
