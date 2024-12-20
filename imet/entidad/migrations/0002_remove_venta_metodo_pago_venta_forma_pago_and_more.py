# Generated by Django 5.1 on 2024-09-29 00:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entidad', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='venta',
            name='metodo_pago',
        ),
        migrations.AddField(
            model_name='venta',
            name='forma_pago',
            field=models.CharField(choices=[('TRAN', 'TRANSFERENCIA'), ('EFEC', 'EFECTIVO'), ('TARJ', 'TARJETA')], default='EFEC', max_length=100),
        ),
        migrations.AddField(
            model_name='venta',
            name='producto',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='entidad.producto'),
        ),
    ]
