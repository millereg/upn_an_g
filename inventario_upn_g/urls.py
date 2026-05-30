"""
URL configuration for inventario_upn_g project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
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
]
