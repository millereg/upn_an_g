from django.urls import path
from . import views

app_name = 'productos'

urlpatterns = [
    path('categoria/', views.categoria_list, name='categoria_list'),
    path('crear-categoria/', views.categoria_create, name='categoria_create'),
    path('editar-categoria/<int:id>/', views.categoria_update, name='categoria_update'),
    path('eliminar-categoria/<int:id>/', views.categoria_delete, name='categoria_delete'),
    path('producto/', views.producto_list, name='producto_list'),
    path('crear-producto/', views.producto_create, name='producto_create'),
    path('editar-producto/<int:id>/', views.producto_update, name='producto_update'),
    path('eliminar-producto/<int:id>/', views.producto_delete, name='producto_delete'),
    path('lote/', views.lote_list, name='lote_list'),
    path('crear-lote/', views.lote_create, name='lote_create'),
    path('editar-lote/<int:id>/', views.lote_update, name='lote_update'),
    path('eliminar-lote/<int:id>/', views.lote_delete, name='lote_delete'),
]
