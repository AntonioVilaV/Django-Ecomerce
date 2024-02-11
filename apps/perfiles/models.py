from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class datosContacto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=11, blank=True, null=True)
    direccion = models.TextField(blank=True, null=True)
    fecha_creada = models.DateTimeField(auto_now_add=True)
