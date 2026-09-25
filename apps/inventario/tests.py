from django.test import TestCase
from django.contrib.auth.models import User
from apps.sucursales.models import Sucursal, Almacen
from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad
from apps.productos.models import Categoria, Producto, Lote
from apps.compras.models import Proveedor
from apps.inventario.models import Inventario
from apps.inventario.views import get_stock_actual, verificar_capacidad


class InventarioViewsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
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

        cls.almacen2 = Almacen.objects.create(
            sucursal=cls.sucursal,
            nombre='Almacén Secundario',
            tipo='secundario',
            capacidad=500,
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

        cls.categoria2 = Categoria.objects.create(
            nombre='Tecnología',
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

        cls.producto3 = Producto.objects.create(
            referencia='TEC001',
            nombre='Laptop HP',
            categoria=cls.categoria2,
            codigo_barra='7891234567892',
            precio=2500.00,
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

        cls.lote3 = Lote.objects.create(
            producto=cls.producto3,
            proveedor=cls.proveedor,
            numero_lote='LOTE003-2026',
            fecha_vencimiento='2027-12-31',
            registro_sanitario='REG-TEC-001',
            estado='activo',
            creado_por=cls.user,
            actualizado_por=cls.user
        )


class GetStockActualTests(InventarioViewsTests):
    def test_get_stock_actual_con_stock(self):
        Inventario.objects.create(almacen=self.almacen, lote=self.lote, cantidad=100)
        result = get_stock_actual(self.almacen)
        self.assertEqual(result, 100)

    def test_get_stock_actual_sin_stock(self):
        result = get_stock_actual(self.almacen)
        self.assertEqual(result, 0)

    def test_get_stock_actual_multiple_lotes(self):
        Inventario.objects.create(almacen=self.almacen, lote=self.lote, cantidad=100)
        Inventario.objects.create(almacen=self.almacen, lote=self.lote2, cantidad=50)
        result = get_stock_actual(self.almacen)
        self.assertEqual(result, 150)

    def test_get_stock_actual_por_almacen(self):
        Inventario.objects.create(almacen=self.almacen, lote=self.lote, cantidad=100)
        Inventario.objects.create(almacen=self.almacen2, lote=self.lote, cantidad=200)
        result_almacen1 = get_stock_actual(self.almacen)
        result_almacen2 = get_stock_actual(self.almacen2)
        self.assertEqual(result_almacen1, 100)
        self.assertEqual(result_almacen2, 200)


class VerificarCapacidadTests(InventarioViewsTests):
    def test_verificar_capacidad_permite_entrada_valida(self):
        Inventario.objects.create(almacen=self.almacen, lote=self.lote, cantidad=100)
        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 100)
        self.assertTrue(puede_agregar)
        self.assertEqual(stock_actual, 100)
        self.assertEqual(capacidad, 1000)

    def test_verificar_capacidad_rechaza_entrada_invalida(self):
        Inventario.objects.create(almacen=self.almacen, lote=self.lote, cantidad=950)
        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 100)
        self.assertFalse(puede_agregar)
        self.assertEqual(stock_actual, 950)
        self.assertEqual(capacidad, 1000)

    def test_verificar_capacidad_en_limite(self):
        Inventario.objects.create(almacen=self.almacen, lote=self.lote, cantidad=900)
        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 100)
        self.assertTrue(puede_agregar)

    def test_verificar_capacidad_almacen_vacio(self):
        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 500)
        self.assertTrue(puede_agregar)
        self.assertEqual(stock_actual, 0)

    def test_verificar_capacidad_exacta(self):
        Inventario.objects.create(almacen=self.almacen, lote=self.lote, cantidad=900)
        puede_agregar, stock_actual, capacidad = verificar_capacidad(self.almacen, 100)
        self.assertTrue(puede_agregar)
        self.assertEqual(stock_actual + 100, capacidad)


class ProductoFiltroTests(InventarioViewsTests):
    def test_filtrar_productos_por_categoria(self):
        productos_oficina = Producto.objects.filter(categoria=self.categoria)
        productos_tec = Producto.objects.filter(categoria=self.categoria2)
        self.assertEqual(productos_oficina.count(), 2)
        self.assertEqual(productos_tec.count(), 1)

    def test_productos_activos(self):
        productos_activos = Producto.objects.filter(estado='activo')
        self.assertGreaterEqual(productos_activos.count(), 3)

    def test_productos_por_estado(self):
        producto_inactivo = Producto.objects.create(
            referencia='OF003',
            nombre='Producto Inactivo',
            categoria=self.categoria,
            precio=100.00,
            estado='inactivo',
            creado_por=self.user,
            actualizado_por=self.user
        )
        activos = Producto.objects.filter(estado='activo')
        inactivos = Producto.objects.filter(estado='inactivo')
        self.assertGreaterEqual(activos.count(), 3)
        self.assertEqual(inactivos.count(), 1)


class LoteFiltroTests(InventarioViewsTests):
    def test_filtrar_lotes_por_producto(self):
        lotes_escritorio = Lote.objects.filter(producto=self.producto)
        self.assertEqual(lotes_escritorio.count(), 1)

    def test_lotes_activos(self):
        lotes_activos = Lote.objects.filter(estado='activo')
        self.assertEqual(lotes_activos.count(), 3)

    def test_lotes_por_fecha_vencimiento(self):
        from datetime import date
        hoy = date.today()
        fecha_limite = date(2027, 12, 31)
        lotes_vigentes = Lote.objects.filter(fecha_vencimiento__gte=hoy, fecha_vencimiento__lte=fecha_limite)
        self.assertEqual(lotes_vigentes.count(), 3)
