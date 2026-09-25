from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('', views.venta_list, name='venta_list'),
    path('crear/', views.venta_create, name='venta_create'),
    path('editar/<int:id>/', views.venta_update, name='venta_update'),
    path('eliminar/<int:id>/', views.venta_delete, name='venta_delete'),
    path('anular/<int:id>/', views.venta_anular, name='venta_anular'),
]
