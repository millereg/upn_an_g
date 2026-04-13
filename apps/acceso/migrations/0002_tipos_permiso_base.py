from django.db import migrations

TIPOS_BASE = [
    (1,  'Ver',            'ver'),
    (2,  'Crear',          'crear'),
    (3,  'Editar',         'editar'),
    (4,  'Eliminar',       'eliminar'),
    (5,  'Ver Reportes',   'ver_reportes'),
    (6,  'Exportar',       'exportar'),
    (7,  'Imprimir',       'imprimir'),
    (8,  'Aprobar',        'aprobar'),
    (9,  'Anular',         'anular'),
]


def crear_tipos(apps, schema_editor):
    TipoPermiso = apps.get_model('acceso', 'TipoPermiso')
    for orden, nombre, codigo in TIPOS_BASE:
        TipoPermiso.objects.get_or_create(codigo=codigo, defaults={'nombre': nombre, 'orden': orden})


def eliminar_tipos(apps, schema_editor):
    TipoPermiso = apps.get_model('acceso', 'TipoPermiso')
    TipoPermiso.objects.filter(codigo__in=[c for _, _, c in TIPOS_BASE]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('acceso', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(crear_tipos, eliminar_tipos),
    ]
