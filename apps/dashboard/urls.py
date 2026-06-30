from django.urls import path
from .views import index, buscar

app_name = 'dashboard'

urlpatterns = [
    path('', index, name='index'),
    path('buscar/', buscar, name='buscar'),
]