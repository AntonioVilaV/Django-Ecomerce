# Generated by Django 3.2.9 on 2022-02-16 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0005_datospago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datosenvio',
            name='cedula',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='direccion',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='nombre',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
    ]