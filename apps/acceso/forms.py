from django import forms
from .models import PermisoModulo


class PermisoModuloForm(forms.ModelForm):
    class Meta:
        model = PermisoModulo
        fields = ['grupo', 'modulo', 'permiso']