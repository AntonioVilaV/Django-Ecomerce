from django.contrib import admin

from apps.venta.models import (
    OperatingStatus,
    PaymentDetails,
    SalesRecord,
    ShippingDetails,
)

# Register your models here.

admin.site.register(SalesRecord)
admin.site.register(OperatingStatus)
admin.site.register(ShippingDetails)
admin.site.register(PaymentDetails)
