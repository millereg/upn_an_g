from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth.models import User
from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad
from apps.productos.models import Categoria, Producto, Lote
from apps.compras.models import Proveedor
from apps.inventario.models import Inventario
from apps.sucursales.models import Almacen


class Command(BaseCommand):
    help = 'Crea categoría, proveedor, productos, lotes y stock'

    def handle(self, *args, **options):
        with transaction.atomic():
            user = User.objects.first()
            pais = Pais.objects.get(codigo='PE')
            depto = Departamento.objects.get(nombre='La Libertad', pais=pais)
            provincia = Provincia.objects.get(nombre='Trujillo', departamento=depto)
            ciudad = Ciudad.objects.get(nombre='Trujillo', provincia=provincia)
            almacen = Almacen.objects.get(nombre='Almacén Principal')

            categoria, _ = Categoria.objects.get_or_create(
                nombre='Oficinas',
                defaults={
                    'estado': 'activo',
                    'creado_por': user,
                    'actualizado_por': user,
                }
            )

            proveedor, _ = Proveedor.objects.get_or_create(
                documento='20123456789',
                defaults={
                    'nombre': 'Distribuidora Norteña S.A.C.',
                    'tipo_documento': 'ruc',
                    'pais': pais,
                    'departamento': depto,
                    'provincia': provincia,
                    'ciudad': ciudad,
                    'direccion': 'Av. Industrial 456',
                    'telefono': '044-456789',
                    'celular': '987654321',
                    'correo': 'ventas@distribuidoranortena.com',
                    'estado': 'activo',
                    'creado_por': user,
                    'actualizado_por': user,
                }
            )

            productos_data = [
                ('OF001', 'Escritorio Ejecutivo', '7891234567890', 850.00),
                ('OF002', 'Silla Ergonomica', '7891234567891', 450.00),
                ('OF003', 'Archivador', '7891234567892', 320.00),
            ]

            lotes = []
            for i, (ref, nombre, barra, precio) in enumerate(productos_data, 1):
                producto, _ = Producto.objects.get_or_create(
                    referencia=ref,
                    defaults={
                        'nombre': nombre,
                        'categoria': categoria,
                        'codigo_barra': barra,
                        'precio': precio,
                        'estado': 'activo',
                        'creado_por': user,
                        'actualizado_por': user,
                    }
                )

                lote, _ = Lote.objects.get_or_create(
                    numero_lote=f'LOTE00{i}-2026',
                    producto=producto,
                    defaults={
                        'proveedor': proveedor,
                        'fecha_vencimiento': '2027-12-31',
                        'registro_sanitario': f'REG-OF-00{i}',
                        'estado': 'activo',
                        'creado_por': user,
                        'actualizado_por': user,
                    }
                )
                lotes.append(lote)

            stock_data = [100, 50, 75]
            for lote, stock in zip(lotes, stock_data):
                Inventario.objects.get_or_create(
                    almacen=almacen,
                    lote=lote,
                    defaults={'cantidad': stock}
                )

            self.stdout.write(self.style.SUCCESS('✓ Categoría: Oficinas | Proveedor: Distribuidora Norteña'))
            self.stdout.write(self.style.SUCCESS('✓ 3 Productos + 3 Lotes + Stock (100, 50, 75)'))
