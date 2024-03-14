# Generated by Django 4.0.3 on 2024-03-14 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperatingStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RegistroVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField(default=1)),
                ('total', models.FloatField(default=1)),
                ('descuento', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('fecha_creada', models.DateTimeField(auto_now_add=True)),
                ('fecha_cierre', models.DateTimeField(blank=True, null=True)),
                ('state', models.BooleanField(default=True)),
                ('estado_operacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.operatingstatus')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venta_product', to='inventory.product')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_creada'],
            },
        ),
        migrations.CreateModel(
            name='datosPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nroRef', models.CharField(max_length=200)),
                ('recibo', models.FileField(upload_to='recibos/')),
                ('fecha_pago', models.DateTimeField()),
                ('fecha_creada', models.DateTimeField(auto_now_add=True)),
                ('venta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='venta.registroventa')),
            ],
        ),
        migrations.CreateModel(
            name='datosEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nroEncomienda', models.CharField(blank=True, max_length=200, null=True)),
                ('nombre', models.CharField(max_length=200)),
                ('cedula', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
                ('direccion', models.TextField()),
                ('fecha_envio', models.DateTimeField(blank=True, null=True)),
                ('fecha_creada', models.DateTimeField(auto_now_add=True)),
                ('venta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venta_datosEnvio', to='venta.registroventa')),
            ],
        ),
    ]
