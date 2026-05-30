from django import forms
from .models import Pais, Departamento, Provincia, Ciudad


class PaisForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre del país...",
            }
        )
    )
    codigo = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ej: PE, US, CO..."}
        )
    )

    class Meta:
        model = Pais
        fields = ["nombre", "codigo"]


class DepartamentoForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre del departamento...",
            }
        )
    )
    pais = forms.ModelChoiceField(
        queryset=Pais.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un país —",
    )

    class Meta:
        model = Departamento
        fields = ["nombre", "pais"]


class ProvinciaForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre de la provincia...",
            }
        )
    )
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un departamento —",
    )

    class Meta:
        model = Provincia
        fields = ["nombre", "departamento"]


class CiudadForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre de la ciudad...",
            }
        )
    )
    provincia = forms.ModelChoiceField(
        queryset=Provincia.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione una provincia —",
    )

    class Meta:
        model = Ciudad
        fields = ["nombre", "provincia"]
