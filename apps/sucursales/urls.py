from django.urls import path
from . import views

app_name = 'sucursales'

urlpatterns = [
    path('sucursal/', views.sucursal_list, name='sucursal_list'),
    path('crear-sucursal/', views.sucursal_create, name='sucursal_create'),
    path('editar-sucursal/<int:id>/', views.sucursal_update, name='sucursal_update'),
    path('eliminar-sucursal/<int:id>/', views.sucursal_delete, name='sucursal_delete'),
    path('almacen/', views.almacen_list, name='almacen_list'),
    path('crear-almacen/', views.almacen_create, name='almacen_create'),
    path('editar-almacen/<int:id>/', views.almacen_update, name='almacen_update'),
    path('eliminar-almacen/<int:id>/', views.almacen_delete, name='almacen_delete'),
]
