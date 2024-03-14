from django.forms import ModelForm, ValidationError

from apps.venta.models import PaymentDetails, SalesRecord, ShippingDetails


class VentaForm(ModelForm):
    class Meta:
        model = SalesRecord
        fields = []


class DetalleVentaForm(ModelForm):
    class Meta:
        model = SalesRecord
        # fields=['operating_status','datos_envios']
        fields = "__all__"


class DatosEnviosForm(ModelForm):
    class Meta:
        model = ShippingDetails
        fields = ["name", "dni", "phone", "address"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit():
            raise ValidationError("El phone debe contener solo numeros")
        else:
            return phone

    def clean_dni(self):
        dni = self.cleaned_data["dni"]
        if not dni.isdigit():
            raise ValidationError("La cedula debe contener solo numeros")
        else:
            return dni


class DatosPagoForm(ModelForm):
    class Meta:
        model = PaymentDetails
        fields = ["ref_no", "receipt", "payment_date"]


class OperatingStatusForm(ModelForm):
    class Meta:
        model = SalesRecord
        fields = ["operating_status"]
