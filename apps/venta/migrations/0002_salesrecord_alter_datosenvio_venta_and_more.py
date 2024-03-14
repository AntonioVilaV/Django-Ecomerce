# Generated by Django 4.0.3 on 2024-03-14 19:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inventory', '0001_initial'),
        ('venta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SalesRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('total', models.FloatField(default=1)),
                ('discount', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('state', models.BooleanField(default=True)),
                ('operating_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='venta.operatingstatus')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venta_product', to='inventory.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
        migrations.AlterField(
            model_name='datosenvio',
            name='venta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='venta_datosEnvio', to='venta.salesrecord'),
        ),
        migrations.AlterField(
            model_name='datospago',
            name='venta',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='venta.salesrecord'),
        ),
        migrations.DeleteModel(
            name='RegistroVenta',
        ),
    ]
