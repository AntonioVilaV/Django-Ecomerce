# Generated by Django 3.2.9 on 2022-02-16 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0009_registroventa_total'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroventa',
            name='cantidad',
            field=models.IntegerField(default=1),
        ),
    ]
