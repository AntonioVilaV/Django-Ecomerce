from django.contrib.auth.models import User
from django.db import models

from apps.inventory.models import Product

# Create your models here.


class OperatingStatus(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class SalesRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="venta_product",
        blank=True,
        null=True,
    )
    quantity = models.IntegerField(default=1)
    total = models.FloatField(default=1)
    discount = models.PositiveSmallIntegerField(null=True, blank=True)
    operating_status = models.ForeignKey(OperatingStatus, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(blank=True, null=True)
    state = models.BooleanField(default=True)

    # operating_status = models.PositiveSmallIntegerField(default=1) #1 en a la espera de pago, 2 en proceso, 3 enviado, 4 entregado.

    def __str__(self):
        return f"| {self.pk} | {self.product.pk} - {self.product.name} | {self.operating_status} | {self.created} "

    class Meta:
        ordering = ["-created"]


class datosEnvio(models.Model):
    venta = models.ForeignKey(
        SalesRecord,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="venta_datosEnvio",
    )
    nroEncomienda = models.CharField(max_length=200, blank=True, null=True)
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    fecha_envio = models.DateTimeField(blank=True, null=True)
    fecha_creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class datosPago(models.Model):
    venta = models.ForeignKey(
        SalesRecord, on_delete=models.CASCADE, blank=True, null=True
    )
    nroRef = models.CharField(max_length=200)
    recibo = models.FileField(upload_to="recibos/")
    fecha_pago = models.DateTimeField()
    fecha_creada = models.DateTimeField(auto_now_add=True)
