from django import forms
from .models import Sucursal, Almacen


class SucursalForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre de la sucursal...",
            }
        )
    )
    codigo = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese el código..."}
        )
    )
    pais = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un país —",
    )
    departamento = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un departamento —",
    )
    provincia = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione una provincia —",
    )
    ciudad = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione una ciudad —",
    )
    direccion = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese la dirección..."}
        )
    )
    referencia = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese una referencia..."}
        )
    )
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese el teléfono..."}
        ),
    )
    celular = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese el celular..."}
        ),
    )
    correo = forms.CharField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el correo electrónico...",
            }
        )
    )
    estado = forms.ChoiceField(
        choices=Sucursal.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad

        self.fields["pais"].queryset = Pais.objects.all()
        self.fields["departamento"].queryset = Departamento.objects.all()
        self.fields["provincia"].queryset = Provincia.objects.all()
        self.fields["ciudad"].queryset = Ciudad.objects.all()

    class Meta:
        model = Sucursal
        fields = [
            "nombre",
            "codigo",
            "pais",
            "departamento",
            "provincia",
            "ciudad",
            "direccion",
            "referencia",
            "telefono",
            "celular",
            "correo",
            "estado",
        ]


class AlmacenForm(forms.ModelForm):
    sucursal = forms.ModelChoiceField(
        queryset=Sucursal.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione una sucursal —",
    )
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre del almacén...",
            }
        )
    )
    tipo = forms.ChoiceField(
        choices=Almacen.TIPO, widget=forms.Select(attrs={"class": "form-control"})
    )
    estado = forms.ChoiceField(
        choices=Almacen.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Almacen
        fields = ["sucursal", "nombre", "tipo", "estado"]
