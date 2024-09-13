from django.shortcuts import render, redirect, get_object_or_404


from django.http import HttpResponse
from entidad.forms import *

from entidad.models import *

# Create your views here.

def productos(request, template_name="entidad/productos.html"):
    productos_list= Producto.objects.all()
    dato={'productos': productos_list}
    return render(request, template_name, dato)