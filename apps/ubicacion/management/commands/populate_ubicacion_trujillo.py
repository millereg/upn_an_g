from django.core.management.base import BaseCommand
from django.db import transaction
from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad


class Command(BaseCommand):
    help = 'Crea ubicación: Trujillo, La Libertad, Perú'

    def handle(self, *args, **options):
        with transaction.atomic():
            pais, _ = Pais.objects.get_or_create(nombre='Perú', codigo='PE')
            depto, _ = Departamento.objects.get_or_create(nombre='La Libertad', pais=pais)
            provincia, _ = Provincia.objects.get_or_create(nombre='Trujillo', departamento=depto)
            ciudad, _ = Ciudad.objects.get_or_create(nombre='Trujillo', provincia=provincia)

            self.stdout.write(self.style.SUCCESS('✓ Trujillo, La Libertad, Perú'))
