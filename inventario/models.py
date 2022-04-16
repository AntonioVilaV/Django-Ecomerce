from django.db import models

from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Categoria(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return '{} - {}'.format(self.pk,self.nombre)

class Producto(models.Model):
    autor = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    nombre = models.CharField(max_length=100)
    precio = models.PositiveIntegerField()
    descripcion = models.TextField()
    foto = models.ImageField(upload_to='product/%Y/%m/%d',null=True,blank=True)
    image_test = models.CharField(max_length=500,null=True,blank=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE,blank=True,null=True)
    estado = models.BooleanField(default=True)
    fecha_creada = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{} - {}'.format(self.pk,self.nombre)

    def get_image(self):
        if self.image_test:
            return self.image_test
        else:
            if self.foto:
                return '{}{}'.format(settings.MEDIA_URL,self.foto)
            return '{}{}'.format(settings.STATIC_URL,'recursos/img/img_empty.jpg')

    def get_descuento(self):
        return hasattr(self,'descuento')

    def sub_total(self):
        if hasattr(self,'descuento'):
            desc = (self.precio * self.descuento.descuento)/100
            return self.precio - desc
        else:
            return self.precio

    class Meta:
        ordering = ["-fecha_creada"]    

class Inventario(models.Model):
    producto = models.OneToOneField(Producto,on_delete=models.CASCADE,related_name="inventario_producto")
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return "{} - | {} - {} | cant = {} |".format(self.pk,self.producto.pk,self.producto.nombre,self.cantidad)


class Descuento(models.Model):
    producto = models.OneToOneField(Producto,on_delete=models.SET_NULL,blank=True,null=True,related_name="descuento")
    descuento = models.PositiveSmallIntegerField(default=1)
    fecha_inicio = models.DateTimeField()
    fecha_cierre = models.DateTimeField()
