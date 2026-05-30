from django import forms
from .models import Modulo, TipoPermiso, PermisoModulo


class ModuloForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre del módulo...",
            }
        )
    )
    codigo = forms.SlugField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: ventas"}
        )
    )
    icono = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: fas fa-shopping-cart"}
        ),
    )
    url = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: ventas:lista"}
        ),
    )
    orden = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Orden en el menú..."}
        )
    )
    padre = forms.ModelChoiceField(
        required=False,
        queryset=Modulo.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Sin módulo padre —",
    )
    estado = forms.ChoiceField(
        choices=Modulo.ESTADO_CHOICES,
        widget=forms.Select(attrs={"class": "form-control"}),
    )

    class Meta:
        model = Modulo
        fields = ["nombre", "codigo", "icono", "url", "orden", "padre", "estado"]


class TipoPermisoForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: Ver Reportes"}
        )
    )
    codigo = forms.SlugField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: ver_reportes"}
        )
    )
    orden = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Orden..."}
        )
    )

    class Meta:
        model = TipoPermiso
        fields = ["nombre", "codigo", "orden"]


class PermisoModuloForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un grupo —",
    )
    modulo = forms.ModelChoiceField(
        queryset=Modulo.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un módulo —",
    )
    permiso = forms.ModelChoiceField(
        queryset=TipoPermiso.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un permiso —",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from django.contrib.auth.models import Group

        self.fields["grupo"].queryset = Group.objects.all()

    class Meta:
        model = PermisoModulo
        fields = ["grupo", "modulo", "permiso"]


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Ingrese su nombre de usuario...",
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control form-control-user",
                "placeholder": "Ingrese su contraseña...",
            }
        )
    )
