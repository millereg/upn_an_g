from django.test import TestCase
from django.contrib.auth.models import User
from apps.sucursales.models import Sucursal, Almacen
from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad
from apps.productos.models import Categoria, Producto, Lote
from apps.compras.models import Proveedor
from apps.inventario.models import Inventario
from apps.inventario.views import get_stock_actual, verificar_capacidad


class InventarioViewsTests(TestCase):
    """Tests para funciones del módulo de inventario"""

    @classmethod
    def setUpTestData(cls):
        """Configuración inicial para todas las pruebas"""
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@test.com'
        )

        cls.pais = Pais.objects.create(nombre='Perú', codigo='PE')
        cls.departamento = Departamento.objects.create(nombre='La Libertad', pais=cls.pais)
        cls.provincia = Provincia.objects.create(nombre='Trujillo', departamento=cls.departamento)
        cls.ciudad = Ciudad.objects.create(nombre='Trujillo', provincia=cls.provincia)

        cls.sucursal = Sucursal.objects.create(
            nombre='Sucursal Centro',
            codigo='SC001',
            pais=cls.pais,
            departamento=cls.departamento,
            provincia=cls.provincia,
            ciudad=cls.ciudad,
            direccion='Av. España 123',
            referencia='Frente al parque central',
            telefono='044-123456',
            celular='987654321',
            correo='sucursal@oficinas.com',
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )

        cls.almacen = Almacen.objects.create(
            sucursal=cls.sucursal,
            nombre='Almacén Principal',
            tipo='principal',
            capacidad=1000,
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )

        cls.categoria = Categoria.objects.create(
            nombre='Oficinas',
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )

        cls.producto = Producto.objects.create(
            referencia='OF001',
            nombre='Escritorio Ejecutivo',
            categoria=cls.categoria,
            codigo_barra='7891234567890',
            requiere_receta=False,
            precio=850.00,
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )

        cls.proveedor = Proveedor.objects.create(
            nombre='Distribuidora Norteña S.A.C.',
            tipo_documento='ruc',
            documento='20123456789',
            pais=cls.pais,
            departamento=cls.departamento,
            provincia=cls.provincia,
            ciudad=cls.ciudad,
            direccion='Av. Industrial 456',
            telefono='044-456789',
            celular='987654321',
            correo='ventas@distribuidoranortena.com',
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )

        cls.lote = Lote.objects.create(
            producto=cls.producto,
            proveedor=cls.proveedor,
            numero_lote='LOTE001-2026',
            fecha_vencimiento='2027-12-31',
            registro_sanitario='REG-OF-001',
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )


class GetStockActualTests(InventarioViewsTests):
    """Tests para la función get_stock_actual()"""

    def test_get_stock_actual_con_stock(self):
        """Debería retornar el stock total de un almacén"""
        Inventario.objects.create(
            almacen=self.almacen,
            lote=self.lote,
            cantidad=100
        )

        result = get_stock_actual(self.almacen)

        self.assertEqual(result, 100)

    def test_get_stock_actual_sin_stock(self):
        """Debería retornar 0 si el almacén no tiene stock"""
        result = get_stock_actual(self.almacen)

        self.assertEqual(result, 0)

    def test_get_stock_actual_multiple_lotes(self):
        """Debería sumar correctamente el stock de múltiples lotes"""
        Inventario.objects.create(
            almacen=self.almacen,
            lote=self.lote,
            cantidad=100
        )

        lote2 = Lote.objects.create(
            producto=self.producto,
            proveedor=self.proveedor,
            numero_lote='LOTE002-2026',
            fecha_vencimiento='2027-12-31',
            registro_sanitario='REG-OF-002',
            estado='activo',
            creado_por=self.user,
            actualizado_por=self.user
        )

        Inventario.objects.create(
            almacen=self.almacen,
            lote=lote2,
            cantidad=50
        )

        result = get_stock_actual(self.almacen)

        self.assertEqual(result, 150)


class VerificarCapacidadTests(InventarioViewsTests):
    """Tests para la función verificar_capacidad()"""

    def test_verificar_capacidad_permite_entrada_valida(self):
        """Debería permitir entrada cuando hay capacidad disponible"""
        Inventario.objects.create(
            almacen=self.almacen,
            lote=self.lote,
            cantidad=100
        )

        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 100)

        self.assertTrue(puede_agregar)
        self.assertEqual(stock_actual, 100)
        self.assertEqual(capacidad, 1000)

    def test_verificar_capacidad_rechaza_entrada_invalida(self):
        """Debería rechazar entrada cuando excede la capacidad"""
        Inventario.objects.create(
            almacen=self.almacen,
            lote=self.lote,
            cantidad=950
        )

        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 100)

        self.assertFalse(puede_agregar)
        self.assertEqual(stock_actual, 950)
        self.assertEqual(capacidad, 1000)

    def test_verificar_capacidad_permite_en_limite(self):
        """Debería permitir entrada exactamente en el límite de capacidad"""
        Inventario.objects.create(
            almacen=self.almacen,
            lote=self.lote,
            cantidad=900
        )

        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 100)

        self.assertTrue(puede_agregar)
        self.assertEqual(stock_actual, 900)

    def test_verificar_capacidad_almacen_vacio(self):
        """Debería permitir entrada completa si el almacén está vacío"""
        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 500)

        self.assertTrue(puede_agregar)
        self.assertEqual(stock_actual, 0)
        self.assertEqual(capacidad, 1000)
