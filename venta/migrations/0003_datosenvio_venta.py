# Generated by Django 3.2.9 on 2022-02-07 16:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0002_remove_datosenvio_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='datosenvio',
            name='venta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='venta.registroventa'),
        ),
    ]
