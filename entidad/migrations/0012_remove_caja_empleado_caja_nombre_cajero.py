# Generated by Django 5.1 on 2024-10-20 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad', '0011_remove_detalleventaxproducto_descrp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='caja',
            name='empleado',
        ),
        migrations.AddField(
            model_name='caja',
            name='nombre_cajero',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]