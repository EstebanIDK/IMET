from django.db import models

from django.contrib.auth.models import User

ESTADOS_CHOICES=(
    ("NOP","NO PAGADO"),
    ("PAG", "PAGADO")
)

METODO_PAGO_CHOICE=(
    ("TRAN","TRANSFERENCIA"),
    ("EFEC", "EFECTIVO"),
    ("TARJ", "TARJETA")
)

class Categoria(models.Model):
    nombre= models.CharField(max_length=50, unique=True, null=False, blank=False)
    
    class Meta:
        verbose_name = ("Categoria")
        verbose_name_plural = ("Categorias")

    def __str__(self):
        return f"{self.nombre}"

class Ciudad(models.Model):
    cp= models.CharField(max_length=4, unique=True, null=False, blank=False)
    nombre= models.CharField(max_length=20, unique=True, null= False, blank=False)
    class Meta:
        verbose_name = ("Ciudad")
        verbose_name_plural = ("Ciudades")

    def __str__(self):
        return f"{self.nombre}({self.cp})"

class Cliente(models.Model):
    dni= models.CharField(max_length=8, unique=True)
    nombre= models.CharField(max_length=30)
    apellido= models.CharField(max_length=30)
    correo= models.EmailField(max_length=40, unique=True, blank=True)
    telefono= models.CharField(max_length=10)
    activo= models.BooleanField(default=True)

    class Meta:
        verbose_name = ("Cliente")
        verbose_name_plural = ("Clientes")

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class ProveedorProducto(models.Model):
    nombre= models.CharField(max_length=100, unique=True)
    telefono= models.CharField(max_length=10, unique=True)
    proveedor= models.ManyToManyField('Producto' ,related_name='proveedores')


    class Meta:
        verbose_name = ("Proveedor de producto")
        verbose_name_plural = ("Proveedores de productos")

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre= models.CharField(max_length=100, blank=False)
    marca= models.CharField(max_length=10, null=True ,blank=True)
    precio= models.DecimalField(max_digits=10, decimal_places=2)
    categoria= models.ForeignKey(Categoria, on_delete=models.PROTECT)
    descripcion= models.TextField(max_length=100, null=True, blank=True)
    cantidad=models.IntegerField(default=0)

    class Meta:
        verbose_name = ("Producto")
        verbose_name_plural = ("Productos")

    def __str__(self):
        return f"{self.nombre} {self.marca} {self.precio} "

class Caja(models.Model):
    empleado= models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_apertura= models.DateTimeField(auto_now_add=True)
    monto_inicial= models.DecimalField(max_digits=10, decimal_places=2)
    total_ingresado= models.DecimalField(max_digits=10, decimal_places=2)
    total_egresado= models.DecimalField(max_digits=10, decimal_places=2)
    saldo_total= models.DecimalField(max_digits=10, decimal_places=2)
    activo= models.BooleanField(default=False)
    class Meta:
        verbose_name = ("Caja")
        verbose_name_plural = ("Cajas")

    def __str__(self):
        return f"{self.empleado.username} {self.fecha_apertura}"

class Venta(models.Model):
    caja= models.ForeignKey(Caja, on_delete=models.PROTECT)
    empleado= models.ForeignKey(User, on_delete=models.PROTECT)
    cliente= models.ForeignKey(Cliente, on_delete=models.PROTECT)
    fecha= models.DateTimeField(auto_now_add=True)
    total= models.DecimalField(max_digits=10, decimal_places=2)
    estado= models.CharField(max_length=4, choices=ESTADOS_CHOICES, default="NOP")
    metodo_pago= models.CharField(max_length=4, choices=METODO_PAGO_CHOICE, default="EFEC")
    class Meta:
        verbose_name = ("Venta")
        verbose_name_plural = ("Ventas")

    def __str__(self):
        return f"{self.caja} {self.empleado.username} {self.cliente} {self.fecha} {self.total} {self.estado}"

class DetalleVenta(models.Model):
    venta= models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad= models.IntegerField()
    sub_total= models.DecimalField(max_digits=10, decimal_places=2)
    producto= models.ManyToManyField(Producto)

    class Meta:
        verbose_name = ("Detalle de venta")
        verbose_name_plural = ("Detalles de ventas")

    def __str__(self):
        return f"{self.producto} {self.cantidad} {self.sub_total}"

class ProveedorServicio(models.Model):
    nombre= models.CharField(max_length=30)
    telefono= models.CharField(max_length=10)
    tipo_de_servicio= models.CharField(max_length=30)

    class Meta:
        verbose_name = ("Proveedor de servicio")
        verbose_name_plural = ("Proveedores de servicios")

    def __str__(self):
        return f"{self.nombre}"

class Servicio(models.Model):
    caja= models.ForeignKey(Caja, on_delete=models.PROTECT)
    proveedor= models.ForeignKey(ProveedorServicio, on_delete=models.PROTECT)
    monto= models.DecimalField(max_digits=10, decimal_places=2)
    fecha_vencimiento= models.DateField()
    fecha_pagado= models.DateTimeField(null=True, blank=True)
    estado= models.CharField(max_length=4, choices=ESTADOS_CHOICES, default="NOP")
    factura= models.CharField(max_length=20)

    class Meta:
        verbose_name = ("Servicio")
        verbose_name_plural = ("Servicios")

    def __str__(self):
        return f"{self.factura} {self.proveedor} {self.estado}"






