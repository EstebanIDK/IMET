# Generated by Django 5.0.6 on 2024-10-22 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad', '0011_remove_detalleventaxproducto_descrp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimientocaja',
            name='tipo',
            field=models.CharField(choices=[('INGRESO', 'Ingreso'), ('RETIRO', 'Retiro'), ('VENTA', 'Venta')], max_length=7),
        ),
    ]
