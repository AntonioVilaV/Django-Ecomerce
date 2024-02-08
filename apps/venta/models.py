from django.db import models

from django.contrib.auth.models import User
from apps.inventario.models import Producto

# Create your models here.

class EstadoOperacion(models.Model):
    nombre=models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class RegistroVenta(models.Model):
    usuario = models.ForeignKey(User,on_delete=models.CASCADE, blank=False, null=False)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE,related_name="venta_producto")
    cantidad = models.IntegerField(default=1)
    total = models.FloatField(default=1)
    descuento = models.PositiveSmallIntegerField(null=True,blank=True)
    estado_operacion = models.ForeignKey(EstadoOperacion,on_delete=models.CASCADE)
    fecha_creada =  models.DateTimeField(auto_now_add=True)
    fecha_cierre =  models.DateTimeField(blank=True,null=True)
    state =  models.BooleanField(default=True)
    
    #estado_operacion = models.PositiveSmallIntegerField(default=1) #1 en a la espera de pago, 2 en proceso, 3 enviado, 4 entregado. 
    
    def __str__(self):
        return '| {} | {} - {} | {} | {} '.format(self.pk,self.producto.pk,self.producto.nombre,self.estado_operacion,self.fecha_creada)

    class Meta:
        ordering = ["-fecha_creada"]

class datosEnvio(models.Model):
    venta = models.ForeignKey(RegistroVenta,on_delete=models.CASCADE,blank=True,null=True,related_name="venta_datosEnvio")
    nroEncomienda = models.CharField(max_length=200,blank=True,null=True)
    nombre = models.CharField(max_length=200)
    cedula = models.CharField(max_length=20)
    telefono = models.CharField(max_length=20)
    direccion= models.TextField()
    fecha_envio =  models.DateTimeField(blank=True,null=True)
    fecha_creada =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

class datosPago(models.Model):
    venta = models.ForeignKey(RegistroVenta,on_delete=models.CASCADE,blank=True,null=True)
    nroRef = models.CharField(max_length=200)
    recibo = models.FileField(upload_to='recibos/')
    fecha_pago = models.DateTimeField()
    fecha_creada =  models.DateTimeField(auto_now_add=True)