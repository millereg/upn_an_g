from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('punto-reorden/', views.reorder_point_report, name='reorder_point'),
    path('asignacion-almacenes/', views.asignacion_almacenes_report, name='asignacion_almacenes'),
    path('planificacion-compras/', views.planification_purchases_report, name='planificacion_compras'),
    path('pronostico/', views.forecasting_report, name='forecasting'),
    path('redistribucion/', views.redistribucion_report, name='redistribucion'),
]
