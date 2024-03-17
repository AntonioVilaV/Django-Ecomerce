from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy

from apps.sale.models import SalesRecord


class ValidateGroup:
    grupo = ""
    url_redirect = ""

    def get_grupo(self):
        return self.grupo

    def get_url_redirect(self):
        if not self.url_redirect:
            return reverse_lazy("ProfileHomeTemplateView")
        else:
            return self.url_redirect

    def dispatch(self, request, *args, **kwargs):
        if request.user.groups.get().name == self.grupo:
            return super().dispatch(request, *args, **kwargs)
        return HttpResponseRedirect(self.get_url_redirect())


class ValidateUser:
    model = ""

    def dispatch(self, request, *args, **kwargs):
        if self.model == "SalesRecord":
            if SalesRecord.objects.get(id=self.kwargs["pk"]).user != self.request.user:
                raise Http404("Producto deshabilitado")
        return super().dispatch(request, *args, **kwargs)
