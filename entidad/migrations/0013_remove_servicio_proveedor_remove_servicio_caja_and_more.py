# Generated by Django 5.0.6 on 2024-10-27 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('entidad', '0012_alter_movimientocaja_tipo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicio',
            name='proveedor',
        ),
        migrations.RemoveField(
            model_name='servicio',
            name='caja',
        ),
        migrations.RenameField(
            model_name='detalleventaxproducto',
            old_name='productos',
            new_name='producto',
        ),
        migrations.DeleteModel(
            name='ProveedorServicio',
        ),
        migrations.DeleteModel(
            name='Servicio',
        ),
    ]
