from django.apps import AppConfig
from django.db.models.signals import post_migrate


def populate_acceso_on_migrate(sender, **kwargs):
    from django.core.management import call_command
    call_command('populate_acceso', verbosity=0)


class AccesoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.acceso'
    verbose_name = 'Control de Acceso'

    def ready(self):
        post_migrate.connect(populate_acceso_on_migrate, sender=self)
