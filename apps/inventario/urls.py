from django.urls import path
from . import views

app_name = 'inventario'

urlpatterns = [
    path('inventario/', views.inventario_list, name='inventario_list'),
    path('eliminar-inventario/<int:id>/', views.inventario_delete, name='inventario_delete'),
    path('movimiento/', views.movimiento_list, name='movimiento_list'),
    path('crear-movimiento/', views.movimiento_create, name='movimiento_create'),
    path('eliminar-movimiento/<int:id>/', views.movimiento_delete, name='movimiento_delete'),
]
