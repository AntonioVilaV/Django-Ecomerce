from django.contrib import admin

from apps.venta.models import OperatingStatus, RegistroVenta, datosEnvio, datosPago

# Register your models here.

admin.site.register(RegistroVenta)
admin.site.register(OperatingStatus)
admin.site.register(datosEnvio)
admin.site.register(datosPago)
