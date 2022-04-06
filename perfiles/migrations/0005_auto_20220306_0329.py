# Generated by Django 3.2.9 on 2022-03-06 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0004_datoscontacto_fecha_creada'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datoscontacto',
            name='correo',
        ),
        migrations.AlterField(
            model_name='datoscontacto',
            name='direccion',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datoscontacto',
            name='telefono',
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
