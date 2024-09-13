from django import forms


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

        def init(self, args, **kwargs):
            super().init(args, **kwargs)
            if self.instance.pk:
                self.fields['proveedores'].initial = self.instance.proveedores.all()

        def save(self, commit=True):
            producto = super().save(commit=False)
            if commit:
                producto.save()
            if 'proveedores' in self.cleaned_data:
                producto.proveedores.set(self.cleaned_data['proveedores'])
            return producto
        


class CategoriaForm(forms.ModelForm):
    class Meta:
        models: Categoria
        field='__all__'