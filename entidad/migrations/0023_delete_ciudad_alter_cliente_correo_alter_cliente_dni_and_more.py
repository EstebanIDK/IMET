# Generated by Django 5.0.6 on 2024-11-25 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad', '0022_alter_proveedorproducto_telefono'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ciudad',
        ),
        migrations.AlterField(
            model_name='cliente',
            name='correo',
            field=models.EmailField(blank=True, max_length=40),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='dni',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='proveedorproducto',
            name='nombre',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='proveedorproducto',
            name='telefono',
            field=models.CharField(max_length=10),
        ),
    ]