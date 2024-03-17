# Generated by Django 4.0.3 on 2024-03-15 00:12

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('perfiles', '0005_auto_20220306_0329'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='datosContacto',
            new_name='ContactDetails',
        ),
        migrations.RenameField(
            model_name='contactdetails',
            old_name='direccion',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='contactdetails',
            old_name='fecha_creada',
            new_name='created',
        ),
        migrations.RenameField(
            model_name='contactdetails',
            old_name='telefono',
            new_name='phone',
        ),
        migrations.RenameField(
            model_name='contactdetails',
            old_name='usuario',
            new_name='user',
        ),
    ]
