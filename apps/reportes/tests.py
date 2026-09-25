from django.test import TestCase
from apps.reportes.views import calcular_eoq, suavizado_exponencial, calcular_redistribucion


class CalcularEOQTests(TestCase):
    """Tests para la función calcular_eoq()"""

    def test_calcular_eoq_con_datos_suficientes(self):
        """Debería calcular EOQ con demanda histórica suficiente"""
        demanda_historica = [100, 120, 110, 130, 125, 115]
        eoq = calcular_eoq(demanda_historica)
        self.assertGreater(eoq, 0)

    def test_calcular_eoq_demanda_cero(self):
        """Debería retornar 0 si la demanda es 0"""
        eoq = calcular_eoq([0, 0, 0, 0, 0, 0])
        self.assertEqual(eoq, 0)

    def test_calcular_eoq_datos_insuficientes(self):
        """Debería retornar 0 si hay menos de 3 datos"""
        eoq = calcular_eoq([100, 120])
        self.assertEqual(eoq, 0)

    def test_calcular_eoq_lista_vacia(self):
        """Debería retornar 0 con lista vacía"""
        eoq = calcular_eoq([])
        self.assertEqual(eoq, 0)


class SuavizadoExponencialTests(TestCase):
    """Tests para la función suavizado_exponencial()"""

    def test_suavizado_exponencial_basico(self):
        """Debería calcular forecast con suavizado exponencial"""
        historico = [10, 12, 15, 14, 18, 20]
        forecast = suavizado_exponencial(historico)
        self.assertGreater(forecast, 0)

    def test_suavizado_exponencial_valor_inicial(self):
        """El forecast debería estar cerca del último valor suavizado"""
        historico = [10, 10, 10, 10]
        forecast = suavizado_exponencial(historico)
        self.assertEqual(forecast, 10)

    def test_suavizado_exponencial_datos_insuficientes(self):
        """Debería retornar 0 con menos de 2 datos"""
        forecast = suavizado_exponencial([10])
        self.assertEqual(forecast, 0)

    def test_suavizado_exponencial_lista_vacia(self):
        """Debería retornar 0 con lista vacía"""
        forecast = suavizado_exponencial([])
        self.assertEqual(forecast, 0)


class CalcularRedistribucionTests(TestCase):
    """Tests para la función calcular_redistribucion()"""

    def test_calcular_redistribucion_sin_congestionados(self):
        """No debería sugerir redistribución si no hay almacenes congestionados"""
        stock_por_almacen = {
            'Almacen A': {'total': 400, 'capacidad': 1000, 'uso_porcentaje': 40},
            'Almacen B': {'total': 300, 'capacidad': 1000, 'uso_porcentaje': 30},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertEqual(len(result), 0)

    def test_calcular_redistribucion_congestion_y_disponible(self):
        """Debería sugerir redistribución de congestionados a disponibles"""
        stock_por_almacen = {
            'Almacen A': {'total': 900, 'capacidad': 1000, 'uso_porcentaje': 90},
            'Almacen B': {'total': 200, 'capacidad': 1000, 'uso_porcentaje': 20},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertGreater(len(result), 0)

    def test_calcular_redistribucion_vacio(self):
        """Debería retornar lista vacía con diccionario vacío"""
        result = calcular_redistribucion({})
        self.assertEqual(len(result), 0)

    def test_calcular_redistribucion_solo_congestion(self):
        """No debería sugerir si todos están congestionados"""
        stock_por_almacen = {
            'Almacen A': {'total': 900, 'capacidad': 1000, 'uso_porcentaje': 90},
            'Almacen B': {'total': 850, 'capacidad': 1000, 'uso_porcentaje': 85},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertEqual(len(result), 0)

    def test_calcular_redistribucion_solo_disponible(self):
        """No debería sugerir si todos tienen espacio disponible"""
        stock_por_almacen = {
            'Almacen A': {'total': 400, 'capacidad': 1000, 'uso_porcentaje': 40},
            'Almacen B': {'total': 300, 'capacidad': 1000, 'uso_porcentaje': 30},
        }
        result = calcular_redistribucion(stock_por_almacen)
        self.assertEqual(len(result), 0)
