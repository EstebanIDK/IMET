from django.shortcuts import render, redirect, get_object_or_404


from django.http import HttpResponse
from entidad.forms import *

from entidad.models import *

# Create your views here.

def productos(request, template_name="entidad/productos.html"):
    productos_list= Producto.objects.all()
    dato={'productos': productos_list}
    return render(request, template_name, dato)

def nuevo_producto(request, template_name="entidad/producto_form.html"):
    if request.method == "POST":
        form= ProductoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("productos")
    else:
        form= ProductoForm()
    dato={"form":form}
    return render(request, template_name, dato)