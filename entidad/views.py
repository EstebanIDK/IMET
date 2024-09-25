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
            Q(nombre__icontains=busqueda) |
            Q(marca__icontains=busqueda)
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
    dato={"form":form,
          "tipo": 'Nuevo'}
    return render(request, template_name, dato)

def modificar_producto(request, pk, template_name="entidad/producto_form.html"):
    producto= Producto.objects.get(id=pk)
    form = ProductoForm(request.POST or None, instance=producto)
    if request.method == "POST":
        if form.is_valid():
            form.save(commit= True)
            return redirect("productos")
    dato={'form': form,
          'dato': ':'+ producto.nombre,
          'tipo': 'Modificar'}
    return render(request, template_name, dato)

def eliminar_producto(request, pk, template_name="entidad/confirmar_eliminacion.html"):
    producto= Producto.objects.get(id=pk)
    if request.method == "POST":
        producto.delete()
        return redirect('productos')
    dato={'objeto': 'el producto',
          'dato': producto.nombre,
          'urls': 'productos'
          }
    return render(request, template_name, dato)

def categorias(request, template_name="entidad/categorias.html"):
    categoria_list= Categoria.objects.all()
    busqueda = request.GET.get('buscar',)
    if busqueda:
        categoria_list = Categoria.objects.filter(
            Q(nombre__icontains=busqueda ) 
        ).distinct()

    dato={'categorias': categoria_list}
    
    return render(request, template_name, dato)


def nueva_categoria(request, template_name="entidad/categoria_form.html"):
    if request.method == "POST":
        form= CategoriaForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("categorias")
    else:
        form= ProductoForm()
    dato={"form":form,
          'tipo': 'Nueva',
          }
    return render(request, template_name, dato)

def modificar_categoria(request, pk, template_name="entidad/categoria_form.html"):
    categoria= Categoria.objects.get(id=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == "POST":
        if form.is_valid():
            form.save(commit= True)
            return redirect("categorias")
    dato ={'form': form,
           'dato': ':'+ categoria.nombre,
           'tipo': 'Modificar'}
    return render(request, template_name, dato)

def eliminar_categoria(request, pk, template_name="entidad/confirmar_eliminacion.html"):
    categoria= Categoria.objects.get(id=pk)
    if request.method == "POST":
        categoria.delete()
        return redirect("categorias")
    dato={'objeto': 'la categoría',
          'dato': categoria.nombre,
          'urls': 'categorias'
          }
    return render(request, template_name, dato)


def proveedores_productos(request, template_name="entidad/proveedores_productos.html"):
    prov_list = ProveedorProducto.objects.all()

    dato ={'proveedores': prov_list}
    return render(request, template_name, dato)

def nuevo_proveedor_producto(request, template_name="entidad/proveedor_producto_form.html"):
    if request.method == 'POST':
        form = ProveedorProductoForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("proveedores_productos")
    else:
        form = ProveedorProductoForm()
    dato = {"form": form,
            'tipo': 'Nuevo'}
    return render(request, template_name, dato)

def modificar_proveedor_producto(request, pk, template_name="entidad/proveedor_producto_form.html"):
    provProd= ProveedorProducto.objects.get(id=pk)
    form = ProveedorProductoForm(request.POST or None, instance=provProd)
    if request.method == "POST":
        if form.is_valid():
            form.save(commit= True)
            return redirect("proveedores_productos")
    dato={'form': form,
          'tipo': 'Modificar',
          'dato': ':' + provProd.nombre}
    return render(request, template_name, dato)

def eliminar_proveedor_producto(request, pk, template_name="entidad/confirmar_eliminacion.html"):
    provProd= ProveedorProducto.objects.get(id=pk)
    if request.method == "POST":
        provProd.delete()
        return redirect("proveedores_productos")
    dato={'objeto': 'el proveedor',
          'dato': provProd.nombre,
          'urls': 'proveedores_productos'
          }
    return render(request, template_name, dato)