from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.pk} - {self.name}"


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=100)
    price = models.PositiveIntegerField()
    description = models.TextField()
    photo = models.ImageField(upload_to="product/%Y/%m/%d", null=True, blank=True)
    image_test = models.CharField(max_length=500, null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return f"{self.pk} - {self.name}"

    def get_image(self):
        if self.image_test:
            return self.image_test
        else:
            if self.photo:
                return f"{settings.MEDIA_URL}{self.photo}"
            return "{}{}".format(settings.STATIC_URL, "recursos/img/img_empty.jpg")

    def get_descuento(self):
        return hasattr(self, "descuento")

    def sub_total(self):
        if hasattr(self, "descuento"):
            desc = (self.price * self.descuento.descuento) / 100
            return self.price - desc
        else:
            return self.price

    class Meta:
        ordering = ["-created"]


class Inventory(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="Inventory_product",
        blank=True,
        null=True,
    )
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{} - | {} - {} | cant = {} |".format(
            self.pk, self.product.pk, self.product.name, self.quantity
        )


class Descuento(models.Model):
    product = models.OneToOneField(
        Product,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="descuento",
    )
    descuento = models.PositiveSmallIntegerField(default=1)
    fecha_inicio = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
