from django import forms
from .models import Venta, DetalleVenta


class VentaForm(forms.ModelForm):
    sucursal = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione una sucursal —",
    )
    almacen = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un almacén —",
    )
    tipo_documento = forms.ChoiceField(
        choices=Venta.TIPO_DOC, widget=forms.Select(attrs={"class": "form-control"})
    )
    numero_documento = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de documento...",
            }
        )
    )
    estado = forms.ChoiceField(
        choices=Venta.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.sucursales.models import Sucursal, Almacen

        self.fields["sucursal"].queryset = Sucursal.objects.all()
        self.fields["almacen"].queryset = Almacen.objects.all()

    class Meta:
        model = Venta
        fields = ["sucursal", "almacen", "tipo_documento", "numero_documento", "estado"]


class DetalleVentaForm(forms.ModelForm):
    lote = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un lote —",
    )
    cantidad = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "Ingrese la cantidad..."}
        )
    )
    precio = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "0.00", "step": "0.01"}
        )
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.productos.models import Lote

        self.fields["lote"].queryset = Lote.objects.all()

    class Meta:
        model = DetalleVenta
        fields = ["lote", "cantidad", "precio"]
