from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name="home"),
    path('permiso_denegado', views.permiso_denegado, name="permiso_denegado"),

    #PRODUCTOS
    path('productos/', views.productos, name="productos"),
    path('nuevo_producto/', views.nuevo_producto, name="nuevo_producto"),
    path('modificar_producto/<int:pk>', views.modificar_producto, name="modificar_producto"),
    path('eliminar_producto/<int:pk>', views.eliminar_producto, name="eliminar_producto"),

    #CATEGORIAS
    path('categorias/', views.categorias, name='categorias'),
    path('nueva_categoria/', views.nueva_categoria, name="nueva_categoria"),
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

    #VENTA   
    path('ventas/nueva/', views.crear_venta, name='crear_venta'),
    path('venta/<int:pk>/', views.detalle_venta, name='detalle_venta'),
    path('detalle_venta_pdf/<int:pk>/', views.detalle_venta_pdf, name='detalle_venta_pdf'),
    path('ventas/', views.ventasactual, name='ventasactual'),
    path('venta_exitosa/<int:pk>/', views.venta_exitosa, name='venta_exitosa'),



    # CLIENTES
    path("clientes", views.clientes, name="clientes"),
    path('nuevo_cliente/', views.nuevo_cliente, name="nuevo_cliente"),
    path("modificar_cliente/<int:pk>",views.modificar_cliente, name="modificar_cliente"),
    path("eliminar_cliente/<int:pk>",views.eliminar_cliente, name="eliminar_cliente"),
    path('ventas_clientes/<int:pk>/ventas', views.ventas_clientes, name='ventas_clientes'),

    #LOGIN
    path("usuarios/", views.usuarios, name='usuarios'),
    path("nuevo_usuario/", views.nuevo_usuario, name='nuevo_usuario'),
    path("modificar_usuario/<int:pk>", views.modificar_usuario, name='modificar_usuario'),
    path("eliminar_usuario/<int:pk>", views.eliminar_usuario, name='eliminar_usuario'), ##CREO QUE NO IRIA EN EL SISTEMA. SOLO PARA PROBAR
    path("login/", views.user_login, name="login"),
    path("logout/", views.login_logout, name='logout'),
    path("change_password/<int:pk>", views.change_password_user, name='change_password'),
    

    
    # GRAFICOS
  
     path('Grafico_clientes/', views.clientes_mas_ventas, name="clientes_mas_ventas"),
     path('grafico_productos/', views.productos_mas_vendidos, name='productos_mas_vendidos'),

]