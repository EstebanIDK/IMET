from django import forms


from entidad.models import *

class ProductoForm(forms.ModelForm):
    class Meta:
        model= Producto
        fields = '__all__'