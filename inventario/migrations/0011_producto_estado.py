# Generated by Django 3.2.9 on 2022-02-16 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0010_producto_fecha_creada'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='estado',
            field=models.BooleanField(default=True),
        ),
    ]
