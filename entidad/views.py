from django.shortcuts import render, redirect, get_object_or_404


from django.http import HttpResponse
from entidad.forms import *

from entidad.models import *

from django.db.models import Q

# Create your views here.

def home(request):
    return render(request, "home.html")

def productos(request, template_name="entidad/productos.html"):
    productos_list= Producto.objects.all()
    busqueda = request.GET.get('buscar',)
    if busqueda:
        productos_list = Producto.objects.filter(
            Q(categoria__nombre__icontains=busqueda ) |
            Q(nombre__icontains=busqueda) 
        ).distinct()

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