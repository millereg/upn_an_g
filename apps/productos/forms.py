from django import forms
from .models import Categoria, Producto, Lote


class CategoriaForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre de la categoría...",
            }
        )
    )
    estado = forms.ChoiceField(
        choices=Categoria.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Categoria
        fields = ["nombre", "estado"]


class ProductoForm(forms.ModelForm):
    referencia = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese la referencia..."}
        )
    )
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre del producto...",
            }
        )
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione una categoría —",
    )
    codigo_barra = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el código de barras...",
            }
        ),
    )
    requiere_receta = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                "class": "form-check-input",
                "style": "margin-top:0.45rem !important;margin-left:0.5rem !important;",
            }
        ),
    )
    precio = forms.DecimalField(
        widget=forms.NumberInput(
            attrs={"class": "form-control", "placeholder": "0.00", "step": "0.01"}
        )
    )
    estado = forms.ChoiceField(
        choices=Producto.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Producto
        fields = [
            "referencia",
            "nombre",
            "categoria",
            "codigo_barra",
            "requiere_receta",
            "precio",
            "estado",
        ]


class LoteForm(forms.ModelForm):
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un producto —",
    )
    proveedor = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un proveedor —",
    )
    numero_lote = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de lote...",
            }
        )
    )
    fecha_vencimiento = forms.DateField(
        widget=forms.DateInput(attrs={"class": "form-control", "type": "date"})
    )
    registro_sanitario = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el registro sanitario...",
            }
        )
    )
    estado = forms.ChoiceField(
        choices=Lote.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.compras.models import Proveedor

        self.fields["proveedor"].queryset = Proveedor.objects.all()

    class Meta:
        model = Lote
        fields = [
            "producto",
            "proveedor",
            "numero_lote",
            "fecha_vencimiento",
            "registro_sanitario",
            "estado",
        ]
