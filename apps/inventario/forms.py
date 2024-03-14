from django import forms
from django.forms import ModelForm

from apps.inventario.models import Inventory, Product


class CreateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = [
            "author",
            "status",
        ]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"onchange": "readURL(this)"}),
        }

    # def clean(self):
    #    nombre = self.cleaned_data.get('nombre',None)
    #    print("####################")
    #    print(nombre)
    #    if nombre.isdigit():
    #        #raise ValidationError("El nombre no puede ser solo numeros")
    #        self.add_error('nombre','El nombre no puede contener solo numeros')
    #    return nombre


class UpdateProductForm(ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        exclude = ["author", "status"]
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"onchange": "readURL(this)"}),
        }


class InventoryForm(ModelForm):
    class Meta:
        model = Inventory
        fields = "__all__"
        exclude = ["product"]
