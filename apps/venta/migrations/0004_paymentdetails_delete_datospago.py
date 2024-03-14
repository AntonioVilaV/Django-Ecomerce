# Generated by Django 4.0.3 on 2024-03-14 20:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('venta', '0003_shippingdetails_alter_salesrecord_product_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_no', models.CharField(max_length=200)),
                ('receipt', models.FileField(upload_to='receipts/')),
                ('payment_date', models.DateTimeField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('sale', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='venta.salesrecord')),
            ],
        ),
        migrations.DeleteModel(
            name='datosPago',
        ),
    ]
