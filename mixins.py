from importlib.resources import path
from django.contrib.auth.models import User
from django.forms import models
from django.http import Http404, HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy

from venta.models import RegistroVenta


class validarGrupo(object):
    grupo = ''
    url_redirect = ''
    
    def get_grupo(self):
        return self.grupo

    def get_url_redirect(self):
        if not self.url_redirect:
            return reverse_lazy('HomePerfilTemplateView')
        else:
            return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.get().name == self.grupo:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_url_redirect())

class validarUsuario(object):
    model = ""
    def dispatch(self, request, *args, **kwargs):
        
        if self.model == "RegistroVenta":
            
            if RegistroVenta.objects.get(id=self.kwargs['pk']).usuario != self.request.user:
                print("############")
                print("aaa")
                raise Http404("Producto deshabilitado")
        return super().dispatch(request, *args, **kwargs)