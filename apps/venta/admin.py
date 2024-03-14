from django.contrib import admin

from apps.venta.models import OperatingStatus, SalesRecord, datosEnvio, datosPago

# Register your models here.

admin.site.register(SalesRecord)
admin.site.register(OperatingStatus)
admin.site.register(datosEnvio)
admin.site.register(datosPago)
