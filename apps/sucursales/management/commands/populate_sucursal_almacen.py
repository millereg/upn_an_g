from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad
from apps.sucursales.models import Sucursal, Almacen


class Command(BaseCommand):
    help = 'Crea sucursal y almacén'

    def handle(self, *args, **options):
        with transaction.atomic():
            user = User.objects.first()
            pais = Pais.objects.get(codigo='PE')
            depto = Departamento.objects.get(nombre='La Libertad', pais=pais)
            provincia = Provincia.objects.get(nombre='Trujillo', departamento=depto)
            ciudad = Ciudad.objects.get(nombre='Trujillo', provincia=provincia)

            sucursal, _ = Sucursal.objects.get_or_create(
                codigo='SC001',
                defaults={
                    'nombre': 'Sucursal Centro',
                    'pais': pais,
                    'departamento': depto,
                    'provincia': provincia,
                    'ciudad': ciudad,
                    'direccion': 'Av. España 123',
                    'referencia': 'Frente al parque central',
                    'telefono': '044-123456',
                    'celular': '987654321',
                    'correo': 'sucursal@oficinas.com',
                    'estado': 'activo',
                    'creado_por': user,
                    'actualizado_por': user,
                }
            )

            almacen, _ = Almacen.objects.get_or_create(
                nombre='Almacén Principal',
                sucursal=sucursal,
                defaults={
                    'tipo': 'principal',
                    'capacidad': 1000,
                    'estado': 'activo',
                    'creado_por': user,
                    'actualizado_por': user,
                }
            )

            self.stdout.write(self.style.SUCCESS('✓ Sucursal Centro + Almacén Principal'))
