from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required,permission_required
from django.core.exceptions import PermissionDenied
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.http import HttpResponse, JsonResponse
from entidad.forms import *

from entidad.models import *

from django.utils import timezone
import json
from decimal import Decimal


from django.contrib import messages
from django.db.models import Sum, Count
from django.db.models.functions import Coalesce
from django.core.serializers.json import DjangoJSONEncoder


# Create your views here.


@login_required
def home(request):
    return render(request, "home.html")

@login_required
def permiso_denegado(request):
    return render(request, "permiso_denegado.html")

@login_required
def productos(request):
    if not request.user.has_perm('entidad.view_producto'):
        return redirect('permiso_denegado')
    productos_list= Producto.objects.all()
    return render(request, "entidad/productos.html", {'productos': productos_list})


@login_required
def nuevo_producto(request):
    if not request.user.has_perm('entidad.add_producto'):
        return redirect('permiso_denegado')
    
    if request.method == "POST":
        nombre= request.POST['nombre']
        marca= request.POST['marca']
        form= ProductoForm(request.POST)
        if Producto.objects.filter(nombre__iexact=nombre, marca__iexact=marca).exists():
            messages.error(request, 'El producto ya existe.')

        elif form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect("productos")
    else:
        form= ProductoForm()
    return render(request, "entidad/producto_form.html", {"form":form,
                                                         "tipo": 'Nuevo'})


@login_required
def modificar_producto(request, pk):
    if not request.user.has_perm('entidad.change_producto'):
        return redirect('permiso_denegado')
    
    producto= Producto.objects.get(id=pk)
    form = ProductoForm(request.POST or None, instance=producto)

    if request.method == "POST":
        nombre= request.POST['nombre']
        marca= request.POST['marca']
        if Producto.objects.filter(nombre__iexact=nombre, marca__iexact=marca).exclude(id=pk).exists():
            messages.error(request, 'El producto ya existe con estos datos.')

        elif form.is_valid():
            form.save(commit= True)
            messages.success(request, 'Producto modificado correctamente.')
            return redirect("productos")
    return render(request, "entidad/producto_form.html", {'form': form,
                                                        'dato': ':'+ producto.nombre,
                                                        'tipo': 'Modificar'})
@login_required
def eliminar_producto(request, pk):
    if not request.user.has_perm('entidad.delete_producto'):
        return redirect('permiso_denegado')

    producto = Producto.objects.get(id=pk)

    if request.method == "POST":
        if DetalleVentaXProducto.objects.filter(producto=producto):
            messages.error(request, 'ERROR! No se puede eliminar el producto porque se encuentra asociado a otros datos.')
        else:
            producto.delete()
            messages.success(request, 'Producto eliminado con éxito.')
            return redirect('productos')  # Redirige a la lista actualizada de productos
    
    # No necesitas una confirmación de vista, solo la lógica para manejar el POST
    return render(request, "entidad/confirmar_eliminacion.html", {
        'objeto': 'el producto',
        'dato': producto.nombre,
        'urls': 'productos'
    })

@login_required
def categorias(request):
    if not request.user.has_perm('entidad.view_categoria'):
        return redirect('permiso_denegado')

    categoria_list= Categoria.objects.all()
    return render(request, "entidad/categorias.html", {'categorias': categoria_list})

@login_required
def nueva_categoria(request):
    if not request.user.has_perm('entidad.add_categoria'):
        return redirect('permiso_denegado')

    if request.method == "POST":
        nombre= request.POST['nombre']
        form= CategoriaForm(request.POST)
        if Categoria.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, 'El producto ya existe.')
        elif form.is_valid():
            categoria = form.save(commit=False)
            categoria.nombre = form.cleaned_data.get('nombre')
            categoria.save()
            messages.success(request, 'Categoria creada correctamente.')
            return redirect("categorias")
    else:
        form= CategoriaForm()
    return render(request, "entidad/categoria_form.html", {"form": form,
                                                        'tipo': 'Nueva'})

@login_required
def modificar_categoria(request, pk):
    if not request.user.has_perm('entidad.change_categoria'):
        return redirect('permiso_denegado')

    categoria= Categoria.objects.get(id=pk)
    form = CategoriaForm(request.POST or None, instance=categoria)
    if request.method == "POST":
        nombre= request.POST['nombre']
        if Categoria.objects.filter(nombre__iexact=nombre).exclude(id=pk).exists():
            messages.error(request, 'Nombre ya existente. Por favor ingrese otro nombre.')
        elif form.is_valid():
            form.save(commit= True)
            messages.success(request, 'Categoria modificada correctamente.')
            return redirect("categorias")
    return render(request, "entidad/categoria_form.html", {'form': form,
                                                        'dato': ':'+ categoria.nombre,
                                                        'tipo': 'Modificar'})


@login_required
def eliminar_categoria(request, pk):
    if not request.user.has_perm('entidad.delete_categoria'):
        return redirect('permiso_denegado')

    categoria = Categoria.objects.get(id=pk)
    if request.method == "POST":
        if Producto.objects.filter(categoria=categoria).exists():
            messages.error(request, 'ERROR! No se puede eliminar la categoría porque está asociada a un producto.')
        else:
            categoria.delete()
            messages.success(request, 'Categoría eliminada con éxito.')
            return redirect('categorias')

    return render(request, "entidad/confirmar_eliminacion.html", {
        'objeto': 'la categoría',
        'dato': categoria.nombre,
        'urls': 'categorias'
    })

@login_required
def proveedores_productos(request):
    if not request.user.has_perm('entidad.view_proveedorproducto'):
        return redirect('permiso_denegado')
    prov_list = ProveedorProducto.objects.all()
    return render(request, "entidad/proveedores_productos.html", {'proveedores': prov_list})



@login_required
def nuevo_proveedor_producto(request):
    if not request.user.has_perm('entidad.add_proveedorproducto'):
        return redirect('permiso_denegado')
    
    if request.method == 'POST':
        nombre= request.POST['nombre']
        form = ProveedorProductoForm(request.POST)
        if ProveedorProducto.objects.filter(nombre__iexact=nombre).exists():
            messages.error(request, 'Proveedor ya existente.')
        elif form.is_valid():
            form.save(commit=True)
            messages.success(request, 'Proveedor creado correctamente.')
            return redirect("proveedores_productos")
    else:
        form = ProveedorProductoForm()
    return render(request, "entidad/proveedor_producto_form.html", {"form": form,
                                                                    'tipo': 'Nuevo'})
@login_required
def modificar_proveedor_producto(request, pk):
    if not request.user.has_perm('entidad.change_proveedorproducto'):
        return redirect('permiso_denegado')
    
    proveedor= ProveedorProducto.objects.get(id=pk)
    form = ProveedorProductoForm(request.POST or None, instance=proveedor)
    if request.method == "POST":
        nombre= request.POST['nombre']
        if ProveedorProducto.objects.filter(nombre__iexact=nombre).exclude(id=pk).exists():
            messages.error(request, 'Nombre de proveedor ya exitente. Por favor ingrese otro nombre.')
        elif form.is_valid():
            form.save(commit= True)
            messages.success(request, 'Proveedor modificado correctamente.')
            return redirect("proveedores_productos")
    return render(request, "entidad/proveedor_producto_form.html", {'form': form,
                                                                'tipo': 'Modificar',
                                                                'dato': ':' + proveedor.nombre})
@login_required
def eliminar_proveedor_producto(request, pk):
    if not request.user.has_perm('entidad.delete_proveedorproducto'):
        return redirect('permiso_denegado')

    proveedor_producto = ProveedorProducto.objects.get(id=pk)
    if request.method == "POST":
        proveedor_producto.delete()
        messages.success(request, 'Proveedor eliminado correctamente')
        return redirect('proveedores_productos')

    return render(request, "entidad/confirmar_eliminacion.html", {
        'objeto': 'el proveedor',
        'dato': proveedor_producto.nombre,
        'urls': 'proveedores_productos'
    })


#CAJA
@login_required
def caja(request):
    if not request.user.has_perm('entidad.view_caja'):
        return redirect('permiso_denegado')
    
    caja = Caja.objects.filter(activo=True).first()
    movimientos = MovimientoCaja.objects.filter(caja=caja)

    #TOTALES DE METODOS DE PAGOS DE LA CAJA ACTUAL
    efectivo= Venta.objects.filter(caja=caja, forma_pago='efectivo')
    total_efectivo=0
    for venta in efectivo:
        total_efectivo += venta.total

    transferencia= Venta.objects.filter(caja=caja, forma_pago='transferencia')
    total_transferencia=0
    for venta in transferencia:
        total_transferencia += venta.total
    
    tarjeta= Venta.objects.filter(caja=caja, forma_pago='tarjeta')
    total_tarjeta=0
    for venta in tarjeta:
        total_tarjeta += venta.total

    return render(request, "entidad/caja.html", {'caja_activa':caja,
                                                'movimientos':movimientos,
                                                'efectivo':total_efectivo,
                                                'transferencia': total_transferencia,
                                                'tarjeta': total_tarjeta})


@login_required
def abrir_caja(request):
    if not request.user.has_perm('entidad.add_caja'):
        return redirect('permiso_denegado')
    
    empleado=request.user
    caja = Caja.objects.filter(activo=True).first()

    if caja:
        # Si ya hay una caja abierta, no se puede abrir otra
        return redirect('caja')
    if request.method=='POST':
        form=AperturaCajaForm(request.POST)
        if form.is_valid():
           monto_inicial = form.cleaned_data["monto_inicial"]
           if monto_inicial <= 0:
                messages.error(request, 'El monto inicial debe ser mayor a 0')
                return render(request, 'entidad/abrir_caja_form.html', {'form': form})
           nueva_caja=Caja.objects.create(empleado=empleado,
           monto_inicial=monto_inicial,
           saldo_total=+monto_inicial,
           activo=True)
           return redirect('caja')
    else:
        form=AperturaCajaForm()
    return render(request, 'entidad/abrir_caja_form.html',{'form':form} )    


@login_required
def  cerrar_caja(request):
    if not request.user.has_perm('entidad.add_caja'):
        return redirect('permiso_denegado')
    
    empleado= request.user
    caja=Caja.objects.filter(activo=True).first()
    if request.method == 'POST':
            caja.activo = False
            caja.fecha_cierre = timezone.now()
            caja.save()
            return redirect('caja')
    return render(request, 'entidad/cerrar_caja.html' , {'caja': caja})

@login_required
def ingresar_dinero(request):
    if not request.user.has_perm('entidad.view_caja'):
        return redirect('permiso_denegado')
    
    empleado=request.user
    caja=Caja.objects.filter(activo=True).first()
    if request.method=='POST':
        form=IngresarDineroForm(request.POST)
        if form.is_valid():
            MovimientoCaja.objects.create(caja=caja,
                                          empleado= empleado,
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

@login_required
def retirar_dinero(request):
    if not request.user.has_perm('entidad.view_caja'):
        return redirect('permiso_denegado')
    
    empleado= request.user
    caja=Caja.objects.filter(activo=True).first()
    if request.method=='POST':
        form= RetirarDineroForm(request.POST)
        if form.is_valid():
            MovimientoCaja.objects.create(caja=caja,
                                          empleado= empleado,
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


@login_required
def cajas(request):
    if not request.user.has_perm('entidad.add_caja'):
        return redirect('permiso_denegado')
    
    caja_list= Caja.objects.all()    
    return render(request, 'entidad/cajas.html', {'cajas': caja_list})

@login_required
def ventas(request, pk):
    if not request.user.has_perm('entidad.add_caja'):
        return redirect('permiso_denegado')
    
    caja= Caja.objects.get(id=pk)
    ventas_list = Venta.objects.filter(caja=caja)
    return render(request, 'entidad/ventas.html', {'ventas': ventas_list,
                                                   'caja': pk})
@login_required
def detalle_venta(request, pk):
    if not request.user.has_perm('entidad.view_detalleventa'):
        return redirect('permiso_denegado')
    
    venta = Venta.objects.get(id=pk)
    detalle_venta = DetalleVenta.objects.get(venta=venta)
    detalle_venta_producto_list = DetalleVentaXProducto.objects.filter(detalle_venta= detalle_venta)
    return render(request, 'entidad/detalle_venta.html', {'venta' : venta,
                                                          'detalle_venta': detalle_venta,
                                                          'dxp': detalle_venta_producto_list})









#VENTAS PRUEBA CHAT

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from decimal import Decimal
import json
import os
from django.conf import settings

def guardar_pdf(html_content, filename):
    pdf_dir = os.path.join(settings.MEDIA_ROOT, 'ventas')
    os.makedirs(pdf_dir, exist_ok=True)
    filepath = os.path.join(pdf_dir, filename)
    
    with open(filepath, 'wb') as pdf_file:
        pisa.CreatePDF(html_content, dest=pdf_file)
    
    return f'ventas/{filename}'

@login_required
def crear_venta(request):
    if not request.user.has_perm('entidad.add_venta'):
        return redirect('permiso_denegado')
    
    if request.method == 'POST':
        # Validar caja abierta
        if not Caja.objects.filter(activo=True).exists():
            messages.error(request, 'No hay caja abierta. Por favor, abra una caja primero.')
            return redirect('crear_venta')
        
        # Obtener datos del formulario
        cliente_id = request.POST.get('cliente')
        if not cliente_id:
            messages.error(request, 'Debe seleccionar un cliente')
            return redirect('crear_venta')
            
        metodo_pago = request.POST.get('metodo_pago')
        productos_json = request.POST.get('productos')
        cantidades_json = request.POST.get('cantidades')
        descuento = Decimal(request.POST.get('descuento', '0'))
        
        productos = json.loads(productos_json)
        cantidades = json.loads(cantidades_json)
        
        # Validar stock
        for i, producto_id in enumerate(productos):
            producto = Producto.objects.get(id=producto_id)
            cantidad = int(cantidades[i])
            if cantidad > producto.cantidad:
                messages.error(request, f'Stock insuficiente para {producto.nombre}')
                return redirect('crear_venta')
        
        # Calcular totales
        total_venta = Decimal('0')
        for i, producto_id in enumerate(productos):
            producto = Producto.objects.get(id=producto_id)
            cantidad = int(cantidades[i])
            total_venta += producto.precio * cantidad
        
        # Aplicar descuento
        total_con_descuento = total_venta - (total_venta * (descuento / Decimal('100')))
        
        try:
            # Crear venta
            caja_actual = Caja.objects.get(activo=True)
            nueva_venta = Venta.objects.create(
                caja=caja_actual,
                cliente_id=cliente_id,
                empleado=request.user,
                total=total_con_descuento,
                forma_pago=metodo_pago,
                descuento=descuento
            )
            
            # Crear detalle de venta
            detalle_venta = DetalleVenta.objects.create(
                venta=nueva_venta,
                sub_total=total_venta,
                cantidad=sum(int(c) for c in cantidades)
            )
            
            # Crear detalles por producto y actualizar stock
            for i, producto_id in enumerate(productos):
                producto = Producto.objects.get(id=producto_id)
                cantidad = int(cantidades[i])
                
                DetalleVentaXProducto.objects.create(
                    detalle_venta=detalle_venta,
                    producto=producto,
                    cantidad=cantidad
                )
                
                # Actualizar stock
                producto.cantidad -= cantidad
                producto.save()
            
            # Actualizar caja
            caja_actual.saldo_total += total_con_descuento
            caja_actual.save()
            
            # Registrar movimiento
            MovimientoCaja.objects.create(
                caja=caja_actual,
                empleado=request.user,
                tipo='VENTA',
                cantidad=total_con_descuento
            )
            
            # Generar PDF
            try:
                template = get_template('entidad/detalle_venta_pdf.html')
                context = {
                    'venta': nueva_venta,
                    'detalle_venta': detalle_venta,
                    'productos': DetalleVentaXProducto.objects.filter(detalle_venta=detalle_venta)
                }
                
                html = template.render(context)
                filename = f'venta_{nueva_venta.id}.pdf'
                pdf_path = guardar_pdf(html, filename)
                
                nueva_venta.pdf_path = pdf_path
                nueva_venta.save()
                
                messages.success(request, 'Venta realizada exitosamente')
            except Exception as e:
                messages.warning(request, f'Venta realizada pero hubo un error al generar el PDF: {str(e)}')
            
            return redirect('ver_venta', venta_id=nueva_venta.id)
            
        except Exception as e:
            messages.error(request, f'Error al procesar la venta: {str(e)}')
            return redirect('crear_venta')
    
    # GET request
    context = {
        'clientes': Cliente.objects.all(),
        'productos': Producto.objects.filter(cantidad__gt=0),
        
    }
    return render(request, 'entidad/crear_venta.html', context)

@login_required
def ver_venta(request, venta_id):
    try:
    venta = Venta.objects.get(id=venta_id)
    detalle_venta = DetalleVenta.objects.get(venta=venta)
    productos = DetalleVentaXProducto.objects.filter(detalle_venta=detalle_venta)
        
        context = {
            'venta': venta,
            'detalle_venta': detalle_venta,
            'productos': productos,
        }
        return render(request, 'entidad/ver_venta.html', context)
    except Venta.DoesNotExist:
        messages.error(request, 'Venta no encontrada')
        return redirect('lista_ventas')

@login_required
def descargar_pdf_venta(request, venta_id):
    try:
        venta = Venta.objects.get(id=venta_id)
        
        if not venta.pdf_path:
            # Si no existe el PDF, regenerarlo
            detalle_venta = DetalleVenta.objects.get(venta=venta)
            productos = DetalleVentaXProducto.objects.filter(detalle_venta=detalle_venta)
            
            template = get_template('entidad/detalle_venta_pdf.html')
            context = {
                'venta': venta,
                'detalle_venta': detalle_venta,
                'productos': productos,
            }
            
            html = template.render(context)
            filename = f'venta_{venta.id}.pdf'
            pdf_path = guardar_pdf(html, filename)
            
            venta.pdf_path = pdf_path
            venta.save()
        
        # Devolver el PDF
        filepath = os.path.join(settings.MEDIA_ROOT, venta.pdf_path)
        if os.path.exists(filepath):
            with open(filepath, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="venta_{venta_id}.pdf"'
                return response
                
        messages.error(request, 'PDF no encontrado')
    except Venta.DoesNotExist:
        messages.error(request, 'Venta no encontrada')
    except Exception as e:
        messages.error(request, f'Error al descargar el PDF: {str(e)}')
    
    return redirect('ver_venta', venta_id=venta_id)

    
@login_required
def ventasactual(request):
    if not request.user.has_perm('entidad.view_venta'):
        return redirect('permiso_denegado')
    
    empleado= request.user
    caja= Caja.objects.get(activo=True)
    ventas_list = Venta.objects.filter(caja=caja)
    return render(request, 'entidad/ventas.html', {'ventas':ventas_list,
                  'caja':caja.id})


# CLIENTES
@login_required
def clientes(request, template_name="entidad/clientes.html"):
    if not request.user.has_perm('entidad.view_cliente'):
        return redirect('permiso_denegado')
    
    cliente_list= Cliente.objects.all()
    dato={"clientes": cliente_list}
    return render(request, template_name, dato)


@login_required
def nuevo_cliente(request):
    if not request.user.has_perm('entidad.add_cliente'):
        return redirect('permiso_denegado')
    
    if request.method == "POST":
        form= ClienteForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect("crear_venta")
    else:
        form= ClienteForm()
    return render(request, "entidad/cliente_form.html", {"form":form})

@login_required
def modificar_cliente(request, pk, template_name="entidad/cliente_form.html"):
    if not request.user.has_perm('entidad.change_cliente'):
        return redirect('permiso_denegado')
    
    cliente= Cliente.objects.get(id=pk)
    form= ClienteForm(request.POST or None, instance=cliente)
    if request.method == "POST":
        if form.is_valid():
            form.save(commit=True)
            return redirect("clientes")
        
    dato={"form": form}
    return render (request, template_name, dato)

@login_required
def eliminar_cliente(request, pk):
    if not request.user.has_perm('entidad.delete_cliente'):
        return redirect('permiso_denegado')
    
    cliente = Cliente.objects.get(id=pk)
    if request.method == "POST":
        cliente.delete()
        messages.success(request, 'Proveedor eliminado correctamente')
        return redirect('clientes')

    return render(request, "entidad/confirmar_eliminacion.html", {
        'objeto': 'el cliente',
        'dato': cliente.nombre,
        'urls': 'clientes'
    })


@login_required
def ventas_clientes(request, pk):
    if not request.user.has_perm('entidad.view_venta'):
        return redirect('permiso_denegado')
    
    cliente = Cliente.objects.get(id=pk)
    ventas = Venta.objects.filter(cliente=cliente)
    return render(request, 'entidad/ventas.html', {'ventas':ventas})




#PROVANDO LOGIN 

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User, Group
from .forms import CustomUserCreationForm


@login_required
def nuevo_usuario(request):
    if not request.user.has_perm('entidad.delete_caja'):
        return redirect('permiso_denegado')
    
    if request.method == 'POST':
        username = request.POST['username']
        form = CustomUserCreationForm(request.POST)
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        elif form.is_valid():
            user = form.save(commit=False)
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email')
            user.save()
            # Asignar el grupo de permisos
            group = form.cleaned_data.get('group')
            user.groups.add(group)
            messages.success(request, 'Account created successfully')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below')
    else:
        form = CustomUserCreationForm()
    return render(request, 'login/usuario_form.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login/login.html')


def login_logout(request):
    logout(request)
    return redirect('login')


#GRAFICOS


def clientes_mas_ventas(request):
    clientes_ventas = (
        Cliente.objects
        .annotate(total_ventas=Count('venta'))
        .order_by('-total_ventas')[:4]
    )
    
    datos_grafico = [
        {
            'name': f"{cliente.nombre} {cliente.apellido}",  
            'ventas': cliente.total_ventas
        }
        for cliente in clientes_ventas
    ]
    
  
    datos_json = json.dumps(datos_grafico, cls=DjangoJSONEncoder)
    
    return render(request, 'entidad/top_ventas.html', {
        'titulo': 'Clientes con mas compras',
        'datos_grafico': datos_json  
    })

def productos_mas_vendidos(request):
  
        productos_ventas = (
            Producto.objects
            .annotate(
                total_vendido=Coalesce(
                    Sum('detalleventaxproducto__cantidad'),
                    0
                )
            )
            .order_by('-total_vendido')[:5]
        )
        
        datos_grafico = [
            {
                'name': f"{producto.nombre} {producto.marca}" if producto.marca else producto.nombre,
                'ventas': int(producto.total_vendido) 
            }
            for producto in productos_ventas
        ]
        
        datos_json = json.dumps(datos_grafico, cls=DjangoJSONEncoder)
        
        return render(request,  'entidad/top_ventas.html', {
            'datos_grafico': datos_json,
            'titulo': 'Productos mas vendidos',
            
        })



def opciones(request):
    return render(request, 'entidad/opciones.html')

def home(request):
    # Obtener productos con stock bajo (menos de 6 unidades)
    productos_stock_bajo = Producto.objects.filter(cantidad__lte=5).order_by('cantidad')
    
    context = {
        'productos_stock_bajo': productos_stock_bajo,
        
    }
    return render(request, 'home.html', context) 