# Generated by Django 3.2.9 on 2022-02-14 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventario', '0003_alter_producto_autor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='cantidad',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='producto',
            name='foto',
            field=models.ImageField(blank=True, default='recursos/img/img_empty.jpg', null=True, upload_to='product/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='producto',
            name='precio',
            field=models.PositiveIntegerField(),
        ),
    ]