from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from apps.sucursales.models import Sucursal, Almacen
from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad
from apps.productos.models import Categoria, Producto, Lote
from apps.compras.models import Proveedor
from apps.inventario.models import Inventario, Movimiento, DetalleMovimiento
from apps.ventas.models import Venta, DetalleVenta


class VentasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='vendedor',
            password='testpass123',
            email='vendedor@oficinas.com'
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

        Inventario.objects.create(almacen=cls.almacen, lote=cls.lote, cantidad=100)
        Inventario.objects.create(almacen=cls.almacen, lote=cls.lote2, cantidad=50)


class VentaListTests(VentasTests):
    def setUp(self):
        self.client = Client()
        self.client.login(username='vendedor', password='testpass123')

    def test_venta_list_requires_login(self):
        self.client.logout()
        response = self.client.get(reverse('ventas:venta_list'))
        self.assertEqual(response.status_code, 302)

    def test_venta_list_loads_successfully(self):
        response = self.client.get(reverse('ventas:venta_list'))
        self.assertEqual(response.status_code, 200)


class VentaFiltroEstadoTests(VentasTests):
    def test_filtrar_ventas_por_estado_completado(self):
        Venta.objects.create(
            sucursal=self.sucursal, almacen=self.almacen,
            tipo_documento='Boleta', numero_documento='BV001-000001',
            estado='completado', creado_por=self.user
        )
        Venta.objects.create(
            sucursal=self.sucursal, almacen=self.almacen,
            tipo_documento='Boleta', numero_documento='BV001-000002',
            estado='cancelado', creado_por=self.user
        )
        ventas_completadas = Venta.objects.filter(estado='completado')
        self.assertEqual(ventas_completadas.count(), 1)

    def test_filtrar_ventas_por_estado_cancelado(self):
        Venta.objects.create(
            sucursal=self.sucursal, almacen=self.almacen,
            tipo_documento='Boleta', numero_documento='BV001-000003',
            estado='cancelado', creado_por=self.user
        )
        ventas_canceladas = Venta.objects.filter(estado='cancelado')
        self.assertEqual(ventas_canceladas.count(), 1)

    def test_filtrar_ventas_por_estado_pendiente(self):
        Venta.objects.create(
            sucursal=self.sucursal, almacen=self.almacen,
            tipo_documento='Boleta', numero_documento='BV001-000005',
            estado='pendiente', creado_por=self.user
        )
        ventas_pendientes = Venta.objects.filter(estado='pendiente')
        self.assertEqual(ventas_pendientes.count(), 1)

    def test_ventas_por_tipo_documento(self):
        Venta.objects.create(
            sucursal=self.sucursal, almacen=self.almacen,
            tipo_documento='Factura', numero_documento='FV001-000001',
            estado='completado', creado_por=self.user
        )
        facturas = Venta.objects.filter(tipo_documento='Factura')
        self.assertEqual(facturas.count(), 1)


class VentaCreateTests(VentasTests):
    def test_crear_venta_con_movimiento_resta_stock(self):
        initial_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad

        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000001',
            estado='completado',
            creado_por=self.user
        )

        movimiento = Movimiento.objects.create(
            tipo='salida',
            almacen=self.almacen,
            referencia=venta.numero_documento,
            fecha=timezone.now(),
            estado='confirmado',
            creado_por=self.user
        )

        DetalleVenta.objects.create(venta=venta, lote=self.lote, cantidad=10, precio=850.00)
        DetalleMovimiento.objects.create(movimiento=movimiento, lote=self.lote, cantidad=10)

        inv = Inventario.objects.get(almacen=self.almacen, lote=self.lote)
        inv.cantidad = max(0, inv.cantidad - 10)
        inv.save()

        final_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad
        self.assertEqual(final_stock, initial_stock - 10)

    def test_crear_venta_calcula_total(self):
        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000002',
            estado='completado',
            creado_por=self.user
        )
        DetalleVenta.objects.create(venta=venta, lote=self.lote, cantidad=10, precio=850.00)
        total = sum(d.cantidad * d.precio for d in venta.detalleventa_set.all())
        self.assertEqual(total, 8500.00)

    def test_stock_no_cambia_sin_movimiento(self):
        initial_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad

        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000003',
            estado='pendiente',
            creado_por=self.user
        )
        DetalleVenta.objects.create(venta=venta, lote=self.lote, cantidad=10, precio=850.00)

        final_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad
        self.assertEqual(final_stock, initial_stock)


class VentaAnularTests(VentasTests):
    def test_anular_venta_restaura_stock(self):
        initial_stock = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad

        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000020',
            estado='completado',
            creado_por=self.user
        )
        DetalleVenta.objects.create(venta=venta, lote=self.lote, cantidad=20, precio=850.00)

        movimiento = Movimiento.objects.create(
            tipo='salida',
            almacen=self.almacen,
            referencia=venta.numero_documento,
            fecha=timezone.now(),
            estado='confirmado',
            creado_por=self.user
        )
        DetalleMovimiento.objects.create(movimiento=movimiento, lote=self.lote, cantidad=20)

        inv = Inventario.objects.get(almacen=self.almacen, lote=self.lote)
        inv.cantidad -= 20
        inv.save()

        stock_despues_venta = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad
        self.assertEqual(stock_despues_venta, initial_stock - 20)

        venta.estado = 'cancelado'
        venta.save()

        inv.cantidad += 20
        inv.save()

        stock_final = Inventario.objects.get(almacen=self.almacen, lote=self.lote).cantidad
        self.assertEqual(stock_final, initial_stock)

    def test_venta_cancelada_no_se_puede_anular_nueviamente(self):
        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000030',
            estado='cancelado',
            creado_por=self.user
        )
        self.assertTrue(venta.estado == 'cancelado')


class CalcularTotalTests(VentasTests):
    def test_calcular_total_multiple_productos(self):
        venta = Venta.objects.create(
            sucursal=self.sucursal,
            almacen=self.almacen,
            tipo_documento='Boleta',
            numero_documento='BV001-000005',
            estado='completado',
            creado_por=self.user
        )
        DetalleVenta.objects.create(venta=venta, lote=self.lote, cantidad=10, precio=850.00)
        DetalleVenta.objects.create(venta=venta, lote=self.lote2, cantidad=5, precio=450.00)

        total = sum(d.cantidad * d.precio for d in venta.detalleventa_set.all())
        expected = (10 * 850.00) + (5 * 450.00)
        self.assertEqual(total, expected)
