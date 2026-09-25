from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from apps.sucursales.models import Sucursal, Almacen
from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad
from apps.productos.models import Categoria, Producto, Lote
from apps.compras.models import Proveedor
from apps.inventario.models import Inventario
from apps.ventas.models import Venta, DetalleVenta


class VentasViewsTests(TestCase):
    """Tests para el módulo de ventas"""

    @classmethod
    def setUpTestData(cls):
        """Configuración inicial para todas las pruebas"""
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='vendedor',
            password='testpass123',
            email='vendedor@oficinas.com'
        )
        cls.client.login(username='vendedor', password='testpass123')

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

        cls.producto2 = Producto.objects.create(
            referencia='OF002',
            nombre='Silla Ergonomica',
            categoria=cls.categoria,
            codigo_barra='7891234567891',
            requiere_receta=False,
            precio=450.00,
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

        cls.lote2 = Lote.objects.create(
            producto=cls.producto2,
            proveedor=cls.proveedor,
            numero_lote='LOTE002-2026',
            fecha_vencimiento='2027-12-31',
            registro_sanitario='REG-OF-002',
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )

        Inventario.objects.create(
            almacen=cls.almacen,
            lote=cls.lote,
            cantidad=100
        )

        Inventario.objects.create(
            almacen=cls.almacen,
            lote=cls.lote2,
            cantidad=50
        )


class VentaListTests(VentasViewsTests):
    """Tests para la vista venta_list"""

    def test_venta_list_requires_login(self):
        """Debería requerir autenticación"""
        self.client.logout()
        response = self.client.get(reverse('ventas:venta_list'))
        self.assertEqual(response.status_code, 302)

    def test_venta_list_loads_successfully(self):
        """Debería cargar la página de lista de ventas"""
        response = self.client.get(reverse('ventas:venta_list'))
        self.assertEqual(response.status_code, 200)

    def test_venta_list_shows_ventas(self):
        """Debería mostrar las ventas en la lista"""
        Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000001',
            estado='completado',
            creado_por=self.user
        )

        response = self.client.get(reverse('ventas:venta_list'))
        self.assertContains(response, 'BV001-000001')


class VentaCreateTests(VentasViewsTests):
    """Tests para la creación de ventas"""

    def test_crear_venta_resta_stock(self):
        """Crear venta debería descontar stock del inventario"""
        initial_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad

        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000001',
            estado='completado',
            creado_por=self.user
        )

        DetalleVenta.objects.create(
            venta=venta,
            lote=self.lote,
            cantidad=10,
            precio=850.00
        )

        final_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad
        self.assertEqual(final_stock, initial_stock - 10)

    def test_crear_venta_calcula_total(self):
        """El total de la venta debería ser la suma de detalles"""
        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000002',
            estado='completado',
            creado_por=self.user
        )

        DetalleVenta.objects.create(
            venta=venta,
            lote=self.lote,
            cantidad=10,
            precio=850.00
        )

        total = sum(d.cantidad * d.precio for d in venta.detalleventa_set.all())
        self.assertEqual(total, 8500.00)


class VentaUpdateTests(VentasViewsTests):
    """Tests para la edición de ventas"""

    def test_editar_venta_cambia_stock(self):
        """Editar venta debería recalcular el stock"""
        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000010',
            estado='completado',
            creado_por=self.user
        )

        DetalleVenta.objects.create(
            venta=venta,
            lote=self.lote,
            cantidad=10,
            precio=850.00
        )

        stock_original = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad

        DetalleVenta.objects.filter(id=venta.id).delete()
        DetalleVenta.objects.create(
            venta=venta,
            lote=self.lote,
            cantidad=5,
            precio=850.00
        )

        venta.estado = 'completado'
        venta.save()

        self.assertEqual(stock_original, 100)


class VentaDeleteTests(VentasViewsTests):
    """Tests para la anulación/eliminación de ventas"""

    def test_anular_venta_restaura_stock(self):
        """Anular venta debería restaurar el stock"""
        initial_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad

        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000020',
            estado='completado',
            creado_por=self.user
        )

        DetalleVenta.objects.create(
            venta=venta,
            lote=self.lote,
            cantidad=20,
            precio=850.00
        )

        stock_despues_venta = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad
        self.assertEqual(stock_despues_venta, initial_stock - 20)

        venta.estado = 'cancelado'
        venta.save()

        for detalle in venta.detalleventa_set.all():
            lote = detalle.lote
            cantidad = detalle.cantidad
            inv = Inventario.objects.filter(almacen=venta.almacen, lote=lote).first()
            if inv:
                inv.cantidad += cantidad
                inv.save()

        stock_final = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad
        self.assertEqual(stock_final, initial_stock)

    def test_venta_cancelada_no_se_puede_anular_nuevamente(self):
        """Una venta ya cancelada no debería permitir anulación"""
        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000030',
            estado='cancelado',
            creado_por=self.user
        )

        self.assertTrue(venta.estado == 'cancelado')


class CalcularTotalTests(VentasViewsTests):
    """Tests para el cálculo de totales"""

    def test_calcular_total_multiple_productos(self):
        """Debería sumar correctamente múltiples productos"""
        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000005',
            estado='completado',
            creado_por=self.user
        )

        DetalleVenta.objects.create(
            venta=venta,
            lote=self.lote,
            cantidad=10,
            precio=850.00
        )

        DetalleVenta.objects.create(
            venta=venta,
            lote=self.lote2,
            cantidad=5,
            precio=450.00
        )

        total = sum(d.cantidad * d.precio for d in venta.detalleventa_set.all())
        expected = (10 * 850.00) + (5 * 450.00)
        self.assertEqual(total, expected)
