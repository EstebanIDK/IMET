from django import forms
from django.forms import modelformset_factory

from entidad.models import *

class ProductoForm(forms.ModelForm):
    proveedores = forms.ModelMultipleChoiceField(
    queryset=ProveedorProducto.objects.all(),
    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
    required=False
    )
    class Meta:
        model = Producto
        fields = ('nombre','marca','precio','categoria','cantidad','descripcion','proveedores')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-styling'}),
            'marca': forms.TextInput(attrs={'class': 'form-styling'}),
            'precio': forms.TextInput(attrs={'class': 'form-styling'}),
            'categoria': forms.Select(attrs={'class': 'form-styling'}),
            'cantidad': forms.TextInput(attrs={'class': 'form-styling'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-styling', 'rows': 3, 'cols': 40}),

        }
        


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields= '__all__'

class ProveedorProductoForm(forms.ModelForm):
    class Meta:
        model = ProveedorProducto
        fields = '__all__'

class AperturaCajaForm(forms.Form):
    monto_inicial=forms.DecimalField(max_digits=10,decimal_places=2)
    

class IngresarDineroForm(forms.Form):
    tipo = forms.ChoiceField(choices=[('INGRESO', 'Ingreso')])
    cantidad=forms.DecimalField(max_digits=10,decimal_places=2)
    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción")

class RetirarDineroForm(forms.Form):
    tipo = forms.ChoiceField(choices=[('RETIRO', 'Retiro')])
    cantidad=forms.DecimalField(max_digits=10,decimal_places=2)
    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción")

#VENTA PRUEBA CHAT
from django import forms
from .models import Venta, DetalleVenta, DetalleVentaXProducto

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'forma_pago']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['cantidad']

class DetalleVentaXProductoForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # Puedes usar otro widget si prefieres algo diferente
        label="Productos"
    )
    cantidad = forms.IntegerField(min_value=1, label="Cantidad por producto")


