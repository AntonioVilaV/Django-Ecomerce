
from django.forms import ModelForm, ValidationError
from apps.venta.models import  RegistroVenta, datosEnvio, datosPago


class VentaForm(ModelForm):
    class Meta:
        model = RegistroVenta
        fields=[]
        

class DetalleVentaForm(ModelForm):
    class Meta:
        model = RegistroVenta
        #fields=['estado_operacion','datos_envios']
        fields="__all__"
            

class DatosEnviosForm(ModelForm):
    class Meta:
        model = datosEnvio
        fields=['nombre','cedula','telefono','direccion']
        
    def clean_telefono(self):
        telefono = self.cleaned_data['telefono']
        if not telefono.isdigit():
            raise ValidationError("El telefono debe contener solo numeros")
        else:
            return telefono
    
    def clean_cedula(self):
        cedula = self.cleaned_data['cedula']
        if not cedula.isdigit():
            raise ValidationError("La cedula debe contener solo numeros")
        else:
            return cedula
    

class DatosPagoForm(ModelForm):
    class Meta:
        model = datosPago
        fields= ['nroRef','recibo','fecha_pago']
        

class EstadoOperacionForm(ModelForm):
    class Meta:
        model = RegistroVenta
        fields = ['estado_operacion']