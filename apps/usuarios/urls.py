from django.urls import path
from . import views

app_name = 'usuarios'

urlpatterns = [
    path('', views.usuario_list, name='usuario_list'),
    path('nuevo/', views.usuario_create, name='usuario_create'),
    path('editar/<int:id>/', views.usuario_update, name='usuario_update'),
    path('eliminar/<int:id>/', views.usuario_delete, name='usuario_delete'),
]
