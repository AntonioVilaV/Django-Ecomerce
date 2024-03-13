from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)

from apps.inventario.forms import CreateProductForm, InventoryForm, UpdateProductForm
from apps.inventario.models import Inventario, Producto
from mixins import validarGrupo

# Create your views here.


# Vendedor - Vistas Productos
class ActivePublicationsListView(LoginRequiredMixin, validarGrupo, ListView):
    """View in charge of displaying the list of Publications or published products that are active. View for user type Seller"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = Producto
    template_name = "perfiles/vendedor/publicaciones/publicaciones.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Active publications"
        return context

    def get_queryset(self):
        return Producto.objects.filter(estado=True).filter(autor=self.request.user)


class PausedPublicationsListView(LoginRequiredMixin, validarGrupo, ListView):
    """View in charge of showing the list of Publications or published products that are paused. View for user type Seller"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = Producto
    template_name = "perfiles/vendedor/publicaciones/publicaciones.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Paused publications"
        return context

    def get_queryset(self):
        return Producto.objects.filter(autor=self.request.user).filter(estado=False)


class PublicationCreateView(LoginRequiredMixin, validarGrupo, CreateView):
    """View in charge of creating product or publication to sell on the platform"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name = "perfiles/vendedor/publicaciones/crearPublicacion.html"
    model = Producto
    form_class = CreateProductForm
    second_form_class = InventoryForm
    success_url = reverse_lazy("HomePerfilTemplateView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Add publication"

        if "form" not in context:
            context["form"] = self.form_class()
        if "form2" not in context:
            context["form2"] = self.second_form_class()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object
        form = self.form_class(request.POST)
        form2 = self.second_form_class(request.POST)

        if form.is_valid() and form2.is_valid():
            inventario = form2.save(commit=False)
            form.instance.autor = self.request.user
            form.instance.estado = True
            if "foto" in self.request.FILES:
                form.instance.foto = self.request.FILES["foto"]
            inventario.producto = form.save()
            inventario.save()

            return redirect(reverse_lazy("ActivePublicationsListView"))
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
            )


class PublicationUpdateView(LoginRequiredMixin, validarGrupo, UpdateView):
    """View in charge of updating or editing the data of a Product"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name = "perfiles/vendedor/publicaciones/updatePublicacion.html"
    model = Producto
    second_model = Inventario
    form_class = UpdateProductForm
    second_form_class = InventoryForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Product not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Update publication"

        producto = self.model.objects.get(id=self.kwargs["pk"])
        inventario = self.second_model.objects.get(producto=producto)

        if "form" not in context:
            context["form"] = self.form_class(instance=producto)
        if "form2" not in context:
            context["form2"] = self.second_form_class(instance=inventario)
        return context

    def post(self, request, *args, **kwargs):
        if self.model.objects.filter(id=self.kwargs["pk"]).filter(
            autor=self.request.user
        ):
            producto = self.model.objects.get(id=self.kwargs["pk"])

            cantidad = self.second_model.objects.get(producto=producto)
            form = self.form_class(request.POST, instance=producto)
            form2 = self.second_form_class(request.POST, instance=cantidad)
            if form.is_valid() and form2.is_valid():
                print(form)
                if "foto" in self.request.FILES:
                    form.instance.foto = self.request.FILES["foto"]
                form.save()
                form2.save()

                if form.instance.estado:
                    self.success_url = reverse_lazy("ActivePublicationsListView")
                else:
                    self.success_url = reverse_lazy("PausedPublicationsListView")

                return redirect(self.get_success_url())
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, form2=form2)
                )
        else:
            raise Http404("Acción denegada")


class PublicationDeleteView(LoginRequiredMixin, validarGrupo, DeleteView):
    """View in charge of deleting product or publication"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = Producto
    template_name = "perfiles/vendedor/publicaciones/eliminarPublicacion.html"
    success_url = reverse_lazy("ActivePublicationsListView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Delete publication"
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.autor == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Product not found")

    def post(self, request, *args, **kwargs):
        if self.object.autor == self.request.user:
            self.object.delete()
            return redirect(reverse_lazy("ActivePublicationsListView"))
        else:
            raise Http404("Action denied")


class ActionPublicationTemplateView(LoginRequiredMixin, validarGrupo, TemplateView):
    """View in charge of managing and executing actions on publications; Activate or pause publication."""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name = "perfiles/vendedor/publicaciones/actionPublicacion.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            producto = Producto.objects.filter(autor=self.request.user).get(
                id=self.kwargs["pk"]
            )
            if self.kwargs["action"] == "pausar" and producto.estado:
                return super().dispatch(request, *args, **kwargs)
            elif self.kwargs["action"] == "activar" and not producto.estado:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Incorrect action")
        except Producto.DoesNotExist:
            raise Http404("Prduct not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        action = self.kwargs["action"]
        title = "Eshop Django -"
        if action[0] == "a":
            title += "Activate publication"
        elif action[0] == "p":
            title += "Pause publication"
        context["title"] = title
        context["action"] = action
        context["producto"] = Producto.objects.get(id=self.kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        producto = Producto.objects.filter(id=self.kwargs["pk"])
        if self.request.user == producto.get().autor:
            if self.kwargs["action"] == "activar":
                if "cantidad" in request.POST:
                    cantidad = request.POST["cantidad"]
                    if cantidad.isdigit() and int(cantidad) > 0:
                        with transaction.atomic():
                            Inventario.objects.filter(producto=producto.get()).update(
                                cantidad=cantidad
                            )
                            producto.update(estado=True)
                            return redirect(reverse_lazy("ActivePublicationsListView"))
                    else:
                        return self.render_to_response(
                            self.get_context_data(
                                error="La cantidad debe ser un numero mayor a 0 para poder activar la publicación"
                            )
                        )
            elif self.kwargs["action"] == "pausar":
                producto.update(estado=False)
                return redirect(reverse_lazy("PausedPublicationsListView"))


# Comprador - Vistas Productos
class ProductDetailView(DetailView):
    """View in charge of displaying product details to the buyer and giving options and purchase details"""

    model = Producto
    template_name = "perfiles/comprador/publicaciones/productoDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        producto = Producto.objects.get(id=self.kwargs["pk"])
        context["title"] = producto.nombre
        context["producto"] = producto
        return context


class ProductSearchListView(ListView):
    """View in charge of showing the list of products resulting from the search in the upper input of the template (grid of products filtered by the search engine)."""

    model = Producto
    template_name = "perfiles/comprador/publicaciones/shop-grid.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - " + self.request.GET["search"]
        context["productosRecientes"] = Producto.objects.filter(estado=True).order_by(
            "-fecha_creada"
        )[:4]
        return context

    def get_queryset(self):
        busqueda = self.request.GET["search"]

        try:
            category = self.request.GET.getlist("categories")[0]
        except IndexError:
            category = "categories"

        if category == "categories":
            return Producto.objects.filter(nombre__icontains=busqueda).filter(
                estado=True
            )
        elif category == "decV":
            return Producto.objects.filter(estado=True).filter(
                descuento__descuento__gte=0
            )
        else:
            return (
                Producto.objects.filter(category__name=category)
                .filter(estado=True)
                .filter(nombre__icontains=busqueda)
            )
