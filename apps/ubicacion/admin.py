from django.contrib import admin
from .models import Pais, Departamento, Provincia, Ciudad

# Register your models here.
admin.site.register(Pais)
admin.site.register(Departamento)
admin.site.register(Provincia)
admin.site.register(Ciudad)