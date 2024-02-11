from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, ValidationError

from apps.perfiles.models import datosContacto


class UpdateDatosContactoForm(ModelForm):
    class Meta:
        model = datosContacto
        fields = ["telefono", "direccion"]

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"]
        if not telefono:
            raise ValidationError("Este campo no puede ser vacío")
        elif not telefono.isdigit():
            raise ValidationError("Solo puede ingresar numeros")
        else:
            return telefono


class UpdateDatosUsuarioForm(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email"]


class RegistroUsuarioForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "groups"]
        labels = {
            "username": "Nombre de usuario",
            "first_name": "Nombre",
            "last_name": "Apellidos",
            "email": "Correo",
            "groups": "Grupos",
        }
