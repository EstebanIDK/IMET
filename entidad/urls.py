from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name="home"),
    #PRODUCTOS
    path('productos/', views.productos, name="productos"),
    path('nuevo_producto/', views.nuevo_producto, name="nuevo_producto"),
    path('modificar_producto/<int:pk>', views.modificar_producto, name="modificar_producto"),
    path('eliminar_producto/<int:pk>', views.eliminar_producto, name="eliminar_producto"),

    #CATEGORIAS
    path('categorias/', views.categorias, name='categorias'),
    path('nueva_categoria/', views.nueva_categoria, name="nueva_categoria"),
    path('nueva_categoria_2/', views.nueva_categoria_2, name="nueva_categoria_2"),

    path('modificar_categoria/<int:pk>', views.modificar_categoria, name="modificar_categoria"),
    path('eliminar_categoria/<int:pk>', views.eliminar_categoria, name="eliminar_categoria"),

    #PROVEEDORES_PRODUCTOS
    path('proveedores_producto/', views.proveedores_productos, name="proveedores_productos"),
    path('nuevo_proveedor_producto/', views.nuevo_proveedor_producto, name="nuevo_proveedor_producto"),
    path('modificar_proveedor_producto/<int:pk>', views.modificar_proveedor_producto, name="modificar_proveedor_producto"),
    path('eliminar_proveedor_producto/<int:pk>', views.eliminar_proveedor_producto, name="eliminar_proveedor_producto"),

    #CAJA
    path('caja',views.caja, name='caja'),
    path('abrir_caja/',views.abrir_caja, name='abrir_caja'),
    path('cerrar_caja/',views.cerrar_caja, name='cerrar_caja'),
    path('ingresar_dinero/',views.ingresar_dinero, name='ingresar_dinero'),
    path('retirar_dinero/',views.retirar_dinero, name='retirar_dinero'),
    path('cajas',views.cajas, name='cajas'),


    path('caja/<int:pk>/ventas', views.ventas, name='ventas'),
    path('venta/<int:pk>/', views.detalle_venta, name='detalle_venta'),


    #VENTA PRUEBA CHAT
    path('ventas/nueva/', views.crear_venta, name='crear_venta'),



]