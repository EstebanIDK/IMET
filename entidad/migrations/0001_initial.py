# Generated by Django 5.0.6 on 2024-09-12 22:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50, unique=True)),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
            },
        ),
        migrations.CreateModel(
            name='Ciudad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cp', models.CharField(max_length=4, unique=True)),
                ('nombre', models.CharField(max_length=20, unique=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dni', models.CharField(max_length=8, unique=True)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('correo', models.EmailField(blank=True, max_length=40, unique=True)),
                ('telefono', models.CharField(max_length=10)),
                ('activo', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
            },
        ),
        migrations.CreateModel(
            name='ProveedorServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=30)),
                ('telefono', models.CharField(max_length=10)),
                ('tipo_de_servicio', models.CharField(max_length=30)),
            ],
            options={
                'verbose_name': 'Proveedor de servicio',
                'verbose_name_plural': 'Proveedores de servicios',
            },
        ),
        migrations.CreateModel(
            name='Caja',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_apertura', models.DateTimeField(auto_now_add=True)),
                ('monto_inicial', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_ingresado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('total_egresado', models.DecimalField(decimal_places=2, max_digits=10)),
                ('saldo_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('activo', models.BooleanField(default=False)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Caja',
                'verbose_name_plural': 'Cajas',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('marca', models.CharField(blank=True, max_length=10, null=True)),
                ('precio', models.DecimalField(decimal_places=2, max_digits=10)),
                ('descripcion', models.TextField(max_length=100)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidad.categoria')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='ProveedorProducto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('telefono', models.CharField(max_length=10, unique=True)),
                ('proveedor', models.ManyToManyField(to='entidad.producto')),
            ],
            options={
                'verbose_name': 'Proveedor de producto',
                'verbose_name_plural': 'Proveedores de productos',
            },
        ),
        migrations.CreateModel(
            name='Servicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha_vencimiento', models.DateField()),
                ('fecha_pagado', models.DateTimeField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('NOP', 'NO PAGADO'), ('PAG', 'PAGADO')], default='NOP', max_length=4)),
                ('factura', models.CharField(max_length=20)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidad.caja')),
                ('proveedor', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidad.proveedorservicio')),
            ],
            options={
                'verbose_name': 'Servicio',
                'verbose_name_plural': 'Servicios',
            },
        ),
        migrations.CreateModel(
            name='Venta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('estado', models.CharField(choices=[('NOP', 'NO PAGADO'), ('PAG', 'PAGADO')], default='NOP', max_length=4)),
                ('metodo_pago', models.CharField(choices=[('TRAN', 'TRANSFERENCIA'), ('EFEC', 'EFECTIVO'), ('TARJ', 'TARJETA')], default='EFEC', max_length=4)),
                ('caja', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidad.caja')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='entidad.cliente')),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
            },
        ),
        migrations.CreateModel(
            name='DetalleVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('sub_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('producto', models.ManyToManyField(to='entidad.producto')),
                ('venta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='entidad.venta')),
            ],
            options={
                'verbose_name': 'Detalle',
                'verbose_name_plural': 'Detalles',
            },
        ),
    ]
