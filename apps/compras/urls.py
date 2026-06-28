from django.urls import path
from . import views

app_name = 'compras'

urlpatterns = [
    path('proveedor/', views.proveedor_list, name='proveedor_list'),
    path('crear-proveedor/', views.proveedor_create, name='proveedor_create'),
    path('editar-proveedor/<int:id>/', views.proveedor_update, name='proveedor_update'),
    path('eliminar-proveedor/<int:id>/', views.proveedor_delete, name='proveedor_delete'),
    path('compra/', views.compra_list, name='compra_list'),
    path('crear-compra/', views.compra_create, name='compra_create'),
    path('editar-compra/<int:id>/', views.compra_update, name='compra_update'),
    path('eliminar-compra/<int:id>/', views.compra_delete, name='compra_delete'),
]