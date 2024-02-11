from django import forms
from django.forms import ModelForm

from apps.inventario.models import Inventario, Producto


class crearProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        exclude = [
            "autor",
            "estado",
        ]
        widgets = {
            "foto": forms.ClearableFileInput(attrs={"onchange": "readURL(this)"}),
        }

    # def clean(self):
    #    nombre = self.cleaned_data.get('nombre',None)
    #    print("####################")
    #    print(nombre)
    #    if nombre.isdigit():
    #        #raise ValidationError("El nombre no puede ser solo numeros")
    #        self.add_error('nombre','El nombre no puede contener solo numeros')
    #    return nombre


class updateProductoForm(ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"
        exclude = ["autor", "estado"]
        widgets = {
            "foto": forms.ClearableFileInput(attrs={"onchange": "readURL(this)"}),
        }


class inventarioForm(ModelForm):
    class Meta:
        model = Inventario
        fields = "__all__"
        exclude = ["producto"]
