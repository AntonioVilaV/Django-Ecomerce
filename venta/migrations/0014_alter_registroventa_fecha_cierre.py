# Generated by Django 3.2.9 on 2022-02-26 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0013_registroventa_fecha_cierre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroventa',
            name='fecha_cierre',
            field=models.DateTimeField(blank=True),
        ),
    ]
