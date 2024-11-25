from django import forms
from django.forms import modelformset_factory

from entidad.models import *

class ProductoForm(forms.ModelForm):
    proveedores = forms.ModelMultipleChoiceField(
    queryset=ProveedorProducto.objects.filter(activo=True),
    widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check'}),
    required=False
    )
    class Meta:
        model = Producto
        fields = ('nombre','marca','precio','categoria','cantidad','descripcion','proveedores')
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-styling'}),
            'marca': forms.TextInput(attrs={'class': 'form-styling'}),
            'precio': forms.NumberInput(attrs={'class': 'form-styling'}),
            'categoria': forms.Select(attrs={'class': 'form-styling'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-styling'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-styling', 'rows': 3, 'cols': 40}),

        }
        


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields= ('nombre',)

class ProveedorProductoForm(forms.ModelForm):
    telefono = forms.CharField(max_length=10, widget= forms.NumberInput(attrs={'max_length': '10', 'oninput': "this.value=this.value.slice(0,10)" , 'placeholder':'Ingrese Teléfono'}), label='Teléfono')
    nombre = forms.CharField(widget=forms.TextInput(attrs={'oninput': "this.value=this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\\s]/g, '')",'placeholder': 'Ingrese nombre proveedor'}),label='Nombre')
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
    dni = forms.CharField(max_length=8, widget= forms.NumberInput(attrs={'max_length': '8', 'oninput': "this.value=this.value.slice(0,8)", 'placeholder': 'Ingrese su DNI'}), label='DNI')
    telefono = forms.CharField(max_length=10, widget= forms.NumberInput(attrs={'max_length': '10', 'oninput': "this.value=this.value.slice(0,10)" , 'placeholder':'Ingrese Teléfono'}), label='Teléfono')
    nombre = forms.CharField(widget=forms.TextInput(attrs={'oninput': "this.value=this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\\s]/g, '')",'placeholder': 'Ingrese su nombre'}),label='Nombre')
    apellido = forms.CharField(widget=forms.TextInput(attrs={'oninput': "this.value=this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\\s]/g, '')",'placeholder': 'Ingrese su apellido'}),label='apellido')
    correo = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'} ), label='Correo Electrónico' )
    class Meta:
        model= Cliente
        fields= ("dni","nombre","apellido","correo","telefono")

#probando formulario de registro

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'oninput': "this.value=this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\\s]/g, '')",'placeholder': 'Ingrese su nombre'}),label='Nombre', required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'oninput': "this.value=this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\\s]/g, '')",'placeholder': 'Ingrese su apellido'}),label='apellido', required= True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'} ), label='Correo Electrónico', required=True)
    group = forms.ModelChoiceField(label='Tipo de usuario', queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'group',)
class UserModifyForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'oninput': "this.value=this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\\s]/g, '')",'placeholder': 'Ingrese su nombre'}),label='Nombre', required=True)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'oninput': "this.value=this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ\\s]/g, '')",'placeholder': 'Ingrese su apellido'}),label='apellido', required= True)
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Ingrese su correo electrónico'} ), label='Correo Electrónico', required=True)
    group = forms.ModelChoiceField(label='Tipo de usuario', queryset=Group.objects.all(), required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'group','is_active',)

