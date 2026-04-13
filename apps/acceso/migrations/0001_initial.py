from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoPermiso',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text="Nombre legible, p.ej. 'Ver Reportes'", max_length=80, unique=True)),
                ('codigo', models.SlugField(help_text="Clave interna, p.ej. 'ver_reportes'", unique=True)),
                ('orden', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Tipo de permiso',
                'verbose_name_plural': 'Tipos de permiso',
                'ordering': ['orden', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Modulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('codigo', models.SlugField(help_text="Identificador único sin espacios, p.ej. 'ventas'", max_length=100, unique=True)),
                ('icono', models.CharField(blank=True, help_text="Clase CSS del ícono, p.ej. 'bi bi-cart'", max_length=80)),
                ('url', models.CharField(blank=True, help_text="Nombre de URL o ruta, p.ej. 'ventas:lista'", max_length=200)),
                ('orden', models.PositiveSmallIntegerField(default=0, help_text='Orden en el menú')),
                ('activo', models.BooleanField(default=True)),
                ('padre', models.ForeignKey(blank=True, help_text='Módulo padre para submenús', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submodulos', to='acceso.modulo')),
            ],
            options={
                'verbose_name': 'Módulo',
                'verbose_name_plural': 'Módulos',
                'ordering': ['orden', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='PermisoModulo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grupo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permisos_modulos', to='auth.group')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='permisos_grupos', to='acceso.modulo')),
                ('permiso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='asignaciones', to='acceso.tipopermiso')),
            ],
            options={
                'verbose_name': 'Permiso de módulo',
                'verbose_name_plural': 'Permisos de módulos',
                'unique_together': {('grupo', 'modulo', 'permiso')},
            },
        ),
    ]
