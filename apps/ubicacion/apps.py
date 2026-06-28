from django.apps import AppConfig
from django.db.models.signals import post_migrate


def populate_ubicacion_on_migrate(sender, **kwargs):
    from django.core.management import call_command
    call_command('populate_ubicacion', '--paises', 'PE', verbosity=0)


class UbicacionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ubicacion'

    def ready(self):
        post_migrate.connect(populate_ubicacion_on_migrate, sender=self)
