from django import forms
from .models import Inventario, Movimiento, DetalleMovimiento


class InventarioForm(forms.ModelForm):
    almacen = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un almacén —",
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.sucursales.models import Almacen
        from apps.productos.models import Lote

        self.fields["almacen"].queryset = Almacen.objects.all()
        self.fields["lote"].queryset = Lote.objects.all()

    class Meta:
        model = Inventario
        fields = ["almacen", "lote", "cantidad"]


class MovimientoForm(forms.ModelForm):
    tipo = forms.ChoiceField(
        choices=Movimiento.TIPO, widget=forms.Select(attrs={"class": "form-control"})
    )
    almacen = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione un almacén —",
    )
    almacen_destino = forms.ModelChoiceField(
        queryset=None,
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label="— Seleccione almacén destino —",
        required=False
    )
    referencia = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Ingrese la referencia..."}
        )
    )
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={"class": "form-control", "type": "datetime-local"}
        )
    )
    estado = forms.ChoiceField(
        choices=Movimiento.ESTADO, widget=forms.Select(attrs={"class": "form-control"})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.sucursales.models import Almacen

        self.fields["almacen"].queryset = Almacen.objects.all()
        self.fields["almacen_destino"].queryset = Almacen.objects.all()

    class Meta:
        model = Movimiento
        fields = ["tipo", "almacen", "almacen_destino", "referencia", "fecha", "estado"]


class DetalleMovimientoForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from apps.productos.models import Lote

        self.fields["lote"].queryset = Lote.objects.all()

    class Meta:
        model = DetalleMovimiento
        fields = ["lote", "cantidad"]
