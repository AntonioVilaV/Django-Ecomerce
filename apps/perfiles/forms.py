from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError

from apps.perfiles.models import ContactDetails


class UpdateDatosContactoForm(ModelForm):
    class Meta:
        model = ContactDetails
        fields = ["phone", "address"]

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone:
            raise ValidationError("Este campo no puede ser vacío")
        elif not phone.isdigit():
            raise ValidationError("Solo puede ingresar numeros")
        else:
            return phone


class UpdateDatosUsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "groups"]
        labels = {
            "username": "Nombre de user",
            "first_name": "Nombre",
            "last_name": "Apellidos",
            "email": "Correo",
            "groups": "Grupos",
        }
