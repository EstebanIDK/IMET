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
        fields= ('nombre',)

class ProveedorProductoForm(forms.ModelForm):
    class Meta:
        model = ProveedorProducto
        fields = ('nombre', 'telefono')

class AperturaCajaForm(forms.Form):
    monto_inicial=forms.DecimalField(max_digits=10, decimal_places=2, required=True)
    

class IngresarDineroForm(forms.Form):
    tipo = forms.ChoiceField(choices=[('INGRESO', 'Ingreso')])
    cantidad=forms.DecimalField(max_digits=10,decimal_places=2, min_value=0, required=True)
    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción")

class RetirarDineroForm(forms.Form):
    tipo = forms.ChoiceField(choices=[('RETIRO', 'Retiro')])
    cantidad=forms.DecimalField(max_digits=10,decimal_places=2, min_value=0, required=True)
    descripcion = forms.CharField(widget=forms.Textarea, required=False, label="Descripción")

class ClienteForm(forms.ModelForm):
    class Meta:
        model= Cliente
        fields= '__all__'
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'correo': 'Correo Electrónico',
            'telefono': 'Teléfono',
            'activo': 'Activo',
        }


#provando formulario de registro

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Nombre', max_length=30, required=True)
    last_name = forms.CharField(label='Apellido', max_length=30, required=True)
    email = forms.EmailField(label='Correo Electrónico', required=True)
    group = forms.ModelChoiceField(label='Tipo de usuario', queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'group')
