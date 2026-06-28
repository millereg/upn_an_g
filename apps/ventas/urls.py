from django.urls import path
from . import views

app_name = 'ventas'

urlpatterns = [
    path('venta/', views.venta_list, name='venta_list'),
    path('crear-venta/', views.venta_create, name='venta_create'),
    path('editar-venta/<int:id>/', views.venta_update, name='venta_update'),
    path('eliminar/<int:id>/', views.venta_delete, name='venta_delete'),
]
