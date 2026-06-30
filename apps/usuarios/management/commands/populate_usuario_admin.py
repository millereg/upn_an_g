from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group
from django.db import transaction


class Command(BaseCommand):
    def handle(self, *args, **options):
        with transaction.atomic():
            user, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'email': 'admin@example.com',
                    'is_staff': True,
                    'is_superuser': True,
                    'is_active': True,
                }
            )
            user.set_password('Password123')
            user.save()

            grupo_desarrollador, _ = Group.objects.get_or_create(name='Desarrollador')
            user.groups.add(grupo_desarrollador)

            if created:
                self.stdout.write(self.style.SUCCESS("Usuario 'admin' creado con grupo Desarrollador"))
            else:
                self.stdout.write(self.style.SUCCESS("Usuario 'admin' actualizado"))
