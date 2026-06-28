from django.urls import path
from . import views

app_name = 'ubicacion'

urlpatterns = [
    path('pais/', views.pais_list, name='pais_list'),
    path('departamento/', views.departamento_list, name='departamento_list'),
    path('provincia/', views.provincia_list, name='provincia_list'),
    path('ciudad/', views.ciudad_list, name='ciudad_list'),
    path('get-departamentos/', views.get_departamentos, name='get_departamentos'),
    path('get-provincias/', views.get_provincias, name='get_provincias'),
    path('get-ciudades/', views.get_ciudades, name='get_ciudades'),
]