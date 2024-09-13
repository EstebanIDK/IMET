from django import forms


from entidad.models import *

class ProductoForm(forms.ModelForm):
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'descripcion-corta', 'rows': 3, 'cols': 40})
    )
    class Meta:
        model = Producto
        fields = '__all__'

class CategoriaForm(forms.ModelForm):
    class Meta:
        models: Categoria
        field='__all__'