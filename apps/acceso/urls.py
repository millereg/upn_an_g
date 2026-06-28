from django.urls import path
from . import views

app_name = 'acceso'

urlpatterns = [
    path('modulo/', views.modulo_list, name='modulo_list'),
    path('eliminar-modulo/<int:id>/', views.modulo_delete, name='modulo_delete'),
    
    path('permiso/', views.permiso_list, name='permiso_list'),
    path('eliminar-permiso/<int:id>/', views.permiso_delete, name='permiso_delete'),
    path('grupo/', views.grupo_list, name='grupo_list'),
    path('crear-grupo/', views.grupo_create, name='grupo_create'),
    path('editar-grupo/<int:id>/', views.grupo_update, name='grupo_update'),
    path('eliminar-grupo/<int:id>/', views.grupo_delete, name='grupo_delete'),
]