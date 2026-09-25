from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Crea usuario admin'

    def handle(self, *args, **options):
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@oficinas.com',
                'is_staff': True,
                'is_superuser': True,
                'is_active': True,
                'first_name': 'Admin',
                'last_name': 'Sistema',
            }
        )
        user.set_password('Password123')
        user.save()

        from django.contrib.auth.models import Group
        grupo = Group.objects.get(id=1)
        user.groups.add(grupo)

        if created:
            self.stdout.write(self.style.SUCCESS("Usuario 'admin' creado con grupo Administrador"))
        else:
            self.stdout.write(self.style.SUCCESS("Usuario 'admin' actualizado"))
