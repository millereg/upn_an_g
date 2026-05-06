from django.urls import path
from . import  views

app_name = 'acceso'

urlpatterns = [
    path('permisos/', views.permission_list, name='permission_list'),
    path('permisos/nuevo', views.permission_create, name='permission_create'),
    path('permisos/editar/<int:id>', views.permission_update, name='permission_update'),
    path('permisos/eliminar/<int:id>', views.permission_delete, name='permission_delete'),
]