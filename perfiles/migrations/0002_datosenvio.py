# Generated by Django 3.2.9 on 2022-02-06 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='datosEnvio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nroEncomienda', models.CharField(max_length=200)),
                ('nombre', models.CharField(max_length=200)),
                ('cedula', models.CharField(max_length=20)),
                ('telefono', models.CharField(max_length=20)),
                ('direccion', models.TextField()),
            ],
        ),
    ]
