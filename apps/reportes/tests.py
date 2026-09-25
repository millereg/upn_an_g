from django.test import TestCase
from apps.reportes.views import calcular_eoq, suavizado_exponencial, calcular_redistribucion


class CalcularEOQTests(TestCase):
    def test_calcular_eoq_con_datos_suficientes(self):
        demanda_historica = [100, 120, 110, 130, 125, 115]
        eoq = calcular_eoq(demanda_historica)
        self.assertGreater(eoq, 0)

    def test_calcular_eoq_demanda_cero(self):
        eoq = calcular_eoq([0, 0, 0, 0, 0, 0])
        self.assertEqual(eoq, 0)

    def test_calcular_eoq_datos_insuficientes(self):
        eoq = calcular_eoq([100, 120])
        self.assertEqual(eoq, 0)

    def test_calcular_eoq_lista_vacia(self):
        eoq = calcular_eoq([])
        self.assertEqual(eoq, 0)

    def test_calcular_eoq_valor_positivo(self):
        demanda_historica = [200, 250, 300, 280, 320, 350]
        eoq = calcular_eoq(demanda_historica)
        self.assertIsNotNone(eoq)


class SuavizadoExponencialTests(TestCase):
    def test_suavizado_exponencial_basico(self):
        historico = [10, 12, 15, 14, 18, 20]
        forecast = suavizado_exponencial(historico)
        self.assertGreater(forecast, 0)

    def test_suavizado_exponencial_valor_inicial(self):
        historico = [10, 10, 10, 10]
        forecast = suavizado_exponencial(historico)
        self.assertEqual(forecast, 10)

    def test_suavizado_exponencial_datos_insuficientes(self):
        forecast = suavizado_exponencial([10])
        self.assertEqual(forecast, 0)

    def test_suavizado_exponencial_lista_vacia(self):
        forecast = suavizado_exponencial([])
        self.assertEqual(forecast, 0)

    def test_suavizado_exponencial_tendencia_creciente(self):
        historico = [100, 110, 120, 130, 140]
        forecast = suavizado_exponencial(historico)
        self.assertGreater(forecast, 100)

    def test_suavizado_exponencial_tendenciaDecreciente(self):
        historico = [200, 180, 160, 140, 120]
        forecast = suavizado_exponencial(historico)
        self.assertLess(forecast, 200)


class CalcularRedistribucionTests(TestCase):
    def test_calcular_redistribucion_sin_congestionados(self):
        stock_por_almacen = {
            'Almacen A': {'total': 400, 'capacidad': 1000, 'uso_porcentaje': 40},
            'Almacen B': {'total': 300, 'capacidad': 1000, 'uso_porcentaje': 30},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertEqual(len(result), 0)

    def test_calcular_redistribucion_congestion_y_disponible(self):
        stock_por_almacen = {
            'Almacen A': {'total': 900, 'capacidad': 1000, 'uso_porcentaje': 90},
            'Almacen B': {'total': 200, 'capacidad': 1000, 'uso_porcentaje': 20},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertGreater(len(result), 0)

    def test_calcular_redistribucion_vacio(self):
        result = calcular_redistribucion({})
        self.assertEqual(len(result), 0)

    def test_calcular_redistribucion_solo_congestion(self):
        stock_por_almacen = {
            'Almacen A': {'total': 900, 'capacidad': 1000, 'uso_porcentaje': 90},
            'Almacen B': {'total': 850, 'capacidad': 1000, 'uso_porcentaje': 85},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertEqual(len(result), 0)

    def test_calcular_redistribucion_solo_disponible(self):
        stock_por_almacen = {
            'Almacen A': {'total': 400, 'capacidad': 1000, 'uso_porcentaje': 40},
            'Almacen B': {'total': 300, 'capacidad': 1000, 'uso_porcentaje': 30},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertEqual(len(result), 0)

    def test_calcular_redistribucion_tres_almacenes(self):
        stock_por_almacen = {
            'Almacen A': {'total': 950, 'capacidad': 1000, 'uso_porcentaje': 95},
            'Almacen B': {'total': 100, 'capacidad': 1000, 'uso_porcentaje': 10},
            'Almacen C': {'total': 500, 'capacidad': 1000, 'uso_porcentaje': 50},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertGreater(len(result), 0)
