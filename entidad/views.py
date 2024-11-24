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

def  cerrar_caja(request):
    empleado= request.user
    caja=Caja.objects.filter(empleado=empleado,activo=True).first()
    if request.method == 'POST':
            caja.activo = False
            caja.save()
            return redirect('caja')
    return render(request, 'entidad/cerrar_caja.html' , {'caja': caja})

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

def ventas(request, pk):
    caja= Caja.objects.get(id=pk)
    ventas_list = Venta.objects.filter(caja=caja)
    return render(request, 'entidad/ventas.html', {'ventas': ventas_list,
                                                   'caja': pk})
def detalle_venta(request, pk):
    venta = Venta.objects.get(id=pk)
    detalle_venta = DetalleVenta.objects.get(venta=venta)
    detalle_venta_producto_list = DetalleVentaXProducto.objects.filter(detalle_venta= detalle_venta)
    return render(request, 'entidad/detalle_venta.html', {'venta' : venta,
                                                          'detalle_venta': detalle_venta,
                                                          'dxp': detalle_venta_producto_list})




#VENTAS PRUEBA CHAT
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Venta, DetalleVenta, DetalleVentaXProducto, Producto,Cliente
from .forms import VentaForm, DetalleVentaForm, DetalleVentaXProductoForm
from django.forms import modelformset_factory





def crear_venta(request):
    empleado = request.user
    caja = Caja.objects.filter(empleado=empleado, activo=True).first()
    
    # Obtener clientes y productos en ambas ramas del flujo
    clientes = Cliente.objects.all()  # Define clientes
    productos = Producto.objects.all()  # Define productos

    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_venta_form = DetalleVentaForm(request.POST)
        productos_form = DetalleVentaXProductoForm(request.POST)

        if venta_form.is_valid() and detalle_venta_form.is_valid() and productos_form.is_valid():
            # Crear la venta
            venta = Venta.objects.create(
                caja=caja,
                empleado=empleado,
                cliente=venta_form.cleaned_data['cliente'],
                total=0,
                forma_pago=venta_form.cleaned_data['forma_pago']
            )

            # Inicializar el total de la venta
            total_venta = 0

            # Crear el detalle de venta
            cantidad = detalle_venta_form.cleaned_data['cantidad']
            detalle_venta = DetalleVenta.objects.create(
                venta=venta,
                cantidad=cantidad,
                sub_total=0  # Inicialmente 0, lo actualizaremos después
            )

            # Obtener los productos seleccionados
            productos = productos_form.cleaned_data['productos']
            cantidad_producto = productos_form.cleaned_data['cantidad']

            # Procesar cada producto seleccionado
            for producto in productos:
                subtotal_producto = producto.precio * cantidad_producto
                total_venta += subtotal_producto

                # Crear la relación entre detalle y producto
                DetalleVentaXProducto.objects.create(
                    detalle_venta=detalle_venta,
                    productos=producto,
                    cantidad=cantidad_producto
                )

            # Actualizar el total de la venta en la instancia de venta
            venta.total = total_venta
            venta.save()

            # Actualizar el saldo total de la caja sumando el total de la venta
            caja.saldo_total += total_venta
            caja.save()

            return redirect('home')  # Redirigir a la lista de ventas o a una vista de confirmación
    else:
        venta_form = VentaForm()
        detalle_venta_form = DetalleVentaForm()
        productos_form = DetalleVentaXProductoForm()

    return render(request, 'entidad/crear_venta.html', {
        'venta_form': venta_form,
        'detalle_venta_form': detalle_venta_form,
        'productos_form': productos_form,
        'clientes': clientes,
        'productos': productos,
    })

