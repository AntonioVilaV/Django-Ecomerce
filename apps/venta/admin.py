from django.contrib import admin

from apps.venta.models import EstadoOperacion, RegistroVenta, datosEnvio, datosPago

# Register your models here.

admin.site.register(RegistroVenta)
admin.site.register(EstadoOperacion)
admin.site.register(datosEnvio)
admin.site.register(datosPago)
