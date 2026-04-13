from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acceso', '0003_alter_tipopermiso_codigo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='modulo',
            name='activo',
        ),
        migrations.AddField(
            model_name='modulo',
            name='estado',
            field=models.CharField(
                choices=[('A', 'Activo'), ('I', 'Inactivo')],
                default='A',
                max_length=1,
            ),
        ),
    ]
