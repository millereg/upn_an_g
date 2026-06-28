"""
URL configuration for inventario_upn_g project.
"""
from django.contrib import admin
from django.urls import path, include
from apps.acceso import views as acceso_views

urlpatterns = [
    path('', acceso_views.login_view, name='login'),
    path('logout/', acceso_views.logout_view, name='logout'),
    path('dashboard/', include('apps.dashboard.urls')),
    path('admin/', admin.site.urls),
    path('acceso/', include('apps.acceso.urls')),
    path('usuarios/', include('apps.usuarios.urls')),
    path('productos/', include('apps.productos.urls')),
    path('compras/', include('apps.compras.urls')),
    path('ventas/', include('apps.ventas.urls')),
    path('inventario/', include('apps.inventario.urls')),
    path('sucursales/', include('apps.sucursales.urls')),
    path('ubicacion/', include('apps.ubicacion.urls')),
]
