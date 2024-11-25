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

def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, id=pk)

    if request.method == "POST":
        producto.delete()
        return redirect('productos')  # Redirige a la lista actualizada de productos

    # No necesitas una confirmación de vista, solo la lógica para manejar el POST
    return redirect('productos')

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
        form= CategoriaForm()
    dato = {
        "form": form,
        'tipo': 'Nueva',
    }
    return render(request, template_name, dato)

def nueva_categoria_2(request, template_name="entidad/categoria_form.html"):
    if request.method == "POST":
        form= CategoriaForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("productos")
    else:
        form= CategoriaForm()
    dato = {
        "form": form,
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
    dato = {'proveedores': prov_list}
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

def eliminar_proveedor_producto(request, pk):
    proveedor_producto = get_object_or_404(ProveedorProducto, id=pk)

    if request.method == "POST":
        proveedor_producto.delete()
        return redirect('proveedores_productos')  # Redirige a la lista actualizada de productos

    # No necesitas una confirmación de vista, solo la lógica para manejar el POST
    return redirect('proveedores_productos')

#CAJA

def caja(request):
    empleado=request.user
    caja_activa=Caja.objects.filter(empleado=empleado,activo=True).first()
    print(caja_activa)
    if caja_activa:
        activo_a='abierta'
    else:
        activo_a='cerrada'
    print(activo_a)
    return render(request, "entidad/caja.html",{'estado':activo_a,'caja_activa':caja_activa} )



def abrir_caja(request):
    empleado=request.user
    if request.method=='POST':
        form=AperturaCajaForm(request.POST)
        if form.is_valid():
           monto_inicial = form.cleaned_data["monto_inicial"]
           nueva_caja=Caja.objects.create(empleado=empleado,
           monto_inicial=monto_inicial,
           saldo_total=+monto_inicial,
           activo=True)
           return redirect('caja')
    else:
        form=AperturaCajaForm()
    return render(request, 'entidad/caja.html',{'form':form} )    

def cerrar_caja(request):
    empleado = request.user
    cajas = Caja.objects.filter(empleado=empleado, activo=True)
    
    if cajas.count() > 1:
        # Handle the scenario where multiple active cajas are found
        caja = cajas.first()
    elif cajas.count() == 1:
        caja = cajas.first()
    else:
        caja = None

    if request.method == 'POST':
        if caja:
            caja.activo = False
            caja.save()
            return redirect('caja')

    return render(request, 'entidad/cerrar_caja.html', {'caja': caja})

def ingresar_dinero(request):
    empleado=request.user
    caja=Caja.objects.filter(empleado=empleado,activo=True).first()
    if request.method=='POST':
        form=IngresarDineroForm(request.POST)
        if form.is_valid():
            MovimientoCaja.objects.create(caja=caja,
                                         tipo=form.cleaned_data["tipo"],
                                         cantidad=form.cleaned_data["cantidad"],
                                        descripcion=form.cleaned_data["descripcion"])
        
            caja.total_ingresado += form.cleaned_data["cantidad"]
            caja.saldo_total += form.cleaned_data["cantidad"]
            caja.save()
            return redirect('caja')
    else:
        form = IngresarDineroForm()
    return render(request,'entidad/ingresar_dinero_form.html', {'form': form})

def retirar_dinero(request):
    empleado= request.user
    caja=Caja.objects.filter(empleado=empleado,activo=True).first()
    if request.method=='POST':
        form= RetirarDineroForm(request.POST)
        if form.is_valid():
            MovimientoCaja.objects.create(caja=caja,
                                         tipo=form.cleaned_data["tipo"],
                                         cantidad=form.cleaned_data["cantidad"],
                                        descripcion=form.cleaned_data["descripcion"])


            caja.total_egresado += form.cleaned_data["cantidad"]
            caja.saldo_total -= form.cleaned_data["cantidad"]
            caja.save()
            return redirect('caja')
    else:
        form = RetirarDineroForm()
    return render(request, 'entidad/retirar_dinero_form.html', {'form':form})

def cajas(request):
    caja_list= Caja.objects.all()
    
    return render(request, 'entidad/cajas.html', {'cajas': caja_list})


#VENTAS PRUEBA CHAT
from django.shortcuts import render, redirect, get_object_or_404
from .models import Caja, Venta, DetalleVenta, DetalleVentaXProducto, Producto
from .forms import VentaForm, DetalleVentaForm, DetalleVentaXProductoForm
from django.db import transaction
from django.utils import timezone


from django.shortcuts import get_object_or_404


def crear_venta(request):
    if request.method == 'POST':
        form_venta = VentaForm(request.POST)
        form_detalle = DetalleVentaForm(request.POST)
        if form_venta.is_valid() and form_detalle.is_valid():
            try:
                # Asignar el empleado autenticado
                venta = form_venta.save(commit=False)
                venta.empleado = request.user
                venta.save()
                
                detalle_venta = form_detalle.save(commit=False)
                detalle_venta.venta = venta
                detalle_venta.save()

                # Obtener el ID del producto desde el POST
                producto_id = request.POST.get('producto')  # Asegúrate de que el nombre del campo es correcto
                producto = get_object_or_404(Producto, id=producto_id)

                # Crear la relación en DetalleVentaXProducto
                DetalleVentaXProducto.objects.create(
                    detalle_venta=detalle_venta,
                    productos=producto,
                    cantidad=detalle_venta.cantidad
                )

                # Registrar la venta en la caja
                caja = venta.caja
                caja.registrar_venta(venta.total)
                
                return redirect('ventas:lista_ventas')
            except Exception as e:
                print(f"Error al guardar la venta: {e}")
                return redirect('home')
        else:
            # Imprimir los errores de los formularios en la consola
            print("Errores en form_venta:", form_venta.errors)
            print("Errores en form_detalle:", form_detalle.errors)
            return redirect('home')
    else:
        form_venta = VentaForm()
        form_detalle = DetalleVentaForm()
    return render(request, 'entidad/crear_venta.html', {'form_venta': form_venta, 'form_detalle': form_detalle})


