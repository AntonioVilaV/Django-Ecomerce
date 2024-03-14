from django.forms import ModelForm, ValidationError

from apps.venta.models import PaymentDetails, SalesRecord, ShippingDetails


class SalesForm(ModelForm):
    class Meta:
        model = SalesRecord
        fields = []


class SalesFormDetail(ModelForm):
    class Meta:
        model = SalesRecord
        # fields=['operating_status','datos_envios']
        fields = "__all__"


class ShippingDataForm(ModelForm):
    class Meta:
        model = ShippingDetails
        fields = ["name", "dni", "phone", "address"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit():
            raise ValidationError("the phone must have only numbers")
        else:
            return phone

    def clean_dni(self):
        dni = self.cleaned_data["dni"]
        if not dni.isdigit():
            raise ValidationError("the dni must contain only numbers")
        else:
            return dni


class PaymentForm(ModelForm):
    class Meta:
        model = PaymentDetails
        fields = ["ref_no", "receipt", "payment_date"]


class OperatingStatusForm(ModelForm):
    class Meta:
        model = SalesRecord
        fields = ["operating_status"]
