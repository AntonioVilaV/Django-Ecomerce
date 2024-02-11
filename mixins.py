from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy

from apps.venta.models import RegistroVenta


class validarGrupo:
    grupo = ""
    url_redirect = ""

    def get_grupo(self):
        return self.grupo

    def get_url_redirect(self):
        if not self.url_redirect:
            return reverse_lazy("HomePerfilTemplateView")
        else:
            return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.get().name == self.grupo:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_url_redirect())


class validarUsuario:
    model = ""

    def dispatch(self, request, *args, **kwargs):
        if self.model == "RegistroVenta":
            if (
                RegistroVenta.objects.get(id=self.kwargs["pk"]).usuario
                != self.request.user
            ):
                print("############")
                print("aaa")
                raise Http404("Producto deshabilitado")
        return super().dispatch(request, *args, **kwargs)
