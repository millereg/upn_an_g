from django import forms
from .models import Proveedor, Compra, DetalleCompra


class ProveedorForm(forms.ModelForm):
    nombre = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el nombre del proveedor...",
            }
        )
    )
    tipo_documento = forms.ChoiceField(
        choices=Proveedor.TIPO_DOC, widget=forms.Select(attrs={"class": "form-control"})
    )
    documento = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ingrese el número de documento...",
            }
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
        choices=Proveedor.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.ubicacion.models import Pais, Departamento, Provincia, Ciudad

        self.fields["pais"].queryset = Pais.objects.all()
        self.fields["departamento"].queryset = Departamento.objects.all()
        self.fields["provincia"].queryset = Provincia.objects.all()
        self.fields["ciudad"].queryset = Ciudad.objects.all()

    class Meta:
        model = Proveedor
        fields = [
            "nombre",
            "tipo_documento",
            "documento",
            "pais",
            "departamento",
            "provincia",
            "ciudad",
            "direccion",
            "telefono",
            "celular",
            "correo",
            "estado",
        ]


class CompraForm(forms.ModelForm):
    proveedor = forms.ModelChoiceField(
        queryset=Proveedor.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un proveedor —",
    )
    almacen = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un almacén —",
    )
    tipo_documento = forms.ChoiceField(
        choices=Compra.TIPO_DOC, widget=forms.Select(attrs={"class": "form-control"})
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
        choices=Compra.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.sucursales.models import Almacen

        self.fields["almacen"].queryset = Almacen.objects.all()

    class Meta:
        model = Compra
        fields = [
            "proveedor",
            "almacen",
            "tipo_documento",
            "numero_documento",
            "estado",
        ]


class DetalleCompraForm(forms.ModelForm):
    compra = forms.ModelChoiceField(
        queryset=Compra.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione una compra —",
    )
    producto = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un producto —",
    )
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
        from apps.productos.models import Producto, Lote

        self.fields["producto"].queryset = Producto.objects.all()
        self.fields["lote"].queryset = Lote.objects.all()

    class Meta:
        model = DetalleCompra
        fields = ["compra", "producto", "lote", "cantidad", "precio"]
