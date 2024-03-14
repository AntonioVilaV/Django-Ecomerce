from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from apps.inventario.models import Inventory, Product
from apps.venta.forms import (
    DatosEnviosForm,
    DatosPagoForm,
    EstadoOperacionForm,
    VentaForm,
)
from apps.venta.models import EstadoOperacion, RegistroVenta, datosEnvio, datosPago
from mixins import validarGrupo

# Create your views here.


# Comprador - Vista Ventas
class ComprarProductoCreateView(LoginRequiredMixin, validarGrupo, CreateView):
    """Vista encargada de mandar la peticion de compra de producto y crear la venta en la base de datos"""

    grupo = "Comprador"
    url_redirect = reverse_lazy("LoginUserLoginView")
    models = RegistroVenta
    template_name = "perfiles/comprador/compras/confirmar_compra.html"
    form_class = VentaForm
    success_url = "/comprar/CompraRealizada/"

    def dispatch(self, request, *args, **kwargs):
        try:
            Product.objects.get(id=self.kwargs["pk"])
        except Product.DoesNotExist:
            raise Http404("Producto no encontrado o perdido")

        if not Product.objects.get(id=self.kwargs["pk"]).status:
            raise Http404("Producto deshabilitado")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs["pk"])
        context["title"] = "Comprar - " + product.name
        context["product"] = product
        return context

    def form_valid(self, form):
        pro = Product.objects.get(id=self.kwargs["pk"])
        cant = 1
        if "quant[1]" in self.request.POST:
            cant = int(self.request.POST["quant[1]"])

            if cant > int(pro.inventory_product.quantity):
                return self.render_to_response(
                    self.get_context_data(
                        quantity_error="Sin stock, ingrese una quantity menor"
                    )
                )  # especificar que debe pedir una quantity menor de productos

        with transaction.atomic():
            form.instance.usuario = self.request.user
            form.instance.product = pro
            discount = 0

            if pro.get_discount():
                form.instance.discount = int(pro.discount.discount)
                discount = (int(pro.price) * cant) * (int(pro.discount.discount) / 100)
            form.instance.cantidad = cant
            form.instance.total = (cant * pro.price) - discount
            form.instance.estado_operacion = EstadoOperacion.objects.get(id=1)
            self.object = form.save()

            inv = Inventory.objects.get(product=pro)
            inv.quantity -= cant
            inv.save()

            if inv.quantity == 0:
                pro.status = False
                pro.save()
            return redirect(reverse_lazy("MisComprasActivasListView"))


class MisComprasActivasListView(LoginRequiredMixin, validarGrupo, ListView):
    """Vista encargada de mostarar lista de las compras activas del usuario. Compras que no tengan status de entregado o cancelado"""

    grupo = "Comprador"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = RegistroVenta
    template_name = "perfiles/comprador/compras/misCompras.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Compras activas"
        return context

    def get_queryset(self):
        return RegistroVenta.objects.filter(usuario=self.request.user.pk).filter(
            state=True
        )


class MisComprasCerradasListView(LoginRequiredMixin, validarGrupo, ListView):
    """Vista encargada de mostarar lista de las compras cerradas del usuario. Compras que tengan status de entregado o cancelado"""

    grupo = "Comprador"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = RegistroVenta
    template_name = "perfiles/comprador/compras/misCompras.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Compras cerrada"
        return context

    def get_queryset(self):
        return RegistroVenta.objects.filter(usuario=self.request.user.pk).filter(
            state=False
        )


class DetalleCompraDetailView(LoginRequiredMixin, TemplateView):
    """Vista encargada de mostrar detalles de compra o factura de compra al usuario"""

    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name = "perfiles/comprador/compras/detalleCompra.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            venta = RegistroVenta.objects.filter(usuario=self.request.user).get(
                id=self.kwargs["pk"]
            )
        except RegistroVenta.DoesNotExist:
            raise Http404("Venta no existe")

        if datosPago.objects.filter(venta__id=venta.id).exists():
            context["datosPago"] = datosPago.objects.get(venta__id=venta.id)
        else:
            context["datosPago"] = "Indefinido"

        if datosEnvio.objects.filter(venta__id=venta.id).exists():
            context["datosEnvio"] = datosEnvio.objects.get(venta__id=venta.id)
        else:
            context["datosEnvio"] = "Indefinido"
        context["title"] = "Compra - " + venta.product.name
        context["venta"] = venta
        return context


class CrearDatosEnvioCreateView(
    LoginRequiredMixin, CreateView
):  # SemiValidado - Recordar decidir cedula
    """Vista encargada de crear los datos de envio del comprador"""

    template_name = "perfiles/comprador/compras/crearDatosEnvio.html"
    model = datosEnvio
    form_class = DatosEnviosForm
    success_url = reverse_lazy("MisVentasActivasListView")

    def dispatch(self, request, *args, **kwargs):
        logeado = self.request.user
        if logeado.is_authenticated:
            if (
                RegistroVenta.objects.filter(id=self.kwargs["pk"])
                .filter(usuario=logeado)
                .exists()
                or RegistroVenta.objects.filter(id=self.kwargs["pk"])
                .filter(product__author=logeado)
                .exists()
            ):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Venta no existe")
        else:
            return redirect(reverse_lazy("HomeIndexTemplateView"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Factura - Datos envío"
        return context

    def form_valid(self, form):
        miVenta = RegistroVenta.objects.get(id=self.kwargs["pk"])
        form.instance.venta = miVenta

        if form.is_valid():
            form.save()
            if self.request.user.groups.get().name == "Vendedor":
                return redirect("/detalleVenta/" + str(miVenta.id))
            elif self.request.user.groups.get().name == "Comprador":
                return redirect("/detalleCompra/" + str(miVenta.id))


class UpdateDatosEnvioUpdateView(LoginRequiredMixin, UpdateView):
    """Vista encargada de editar o actualizar en los datos de envio del comprador en la compra realizada"""

    template_name = "perfiles/comprador/compras/updateDatosEnvio.html"
    model = datosEnvio
    form_class = DatosEnviosForm
    success_url = reverse_lazy("HomePerfilTemplateView")

    def get_object(self, queryset=None):
        logeado = self.request.user
        if (
            RegistroVenta.objects.filter(id=self.kwargs["pk"])
            .filter(usuario=logeado)
            .exists()
            or RegistroVenta.objects.filter(id=self.kwargs["pk"])
            .filter(product__author=logeado)
            .exists()
        ):
            return datosEnvio.objects.get(venta__id=self.kwargs["pk"])

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("Datos no existe")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Factura - Datos envío"
        return context

    def form_valid(self, form):
        venta = RegistroVenta.objects.get(id=self.kwargs["pk"])
        if form.is_valid():
            form.save()
            if self.request.user.groups.get().name == "Vendedor":
                return redirect("/detalleVenta/" + str(venta.id))
            elif self.request.user.groups.get().name == "Comprador":
                return redirect("/detalleCompra/" + str(venta.id))


class CrearDatosPagoCreateView(LoginRequiredMixin, CreateView):  # Validado
    """Vista encargada de agregar los recibos y datos del pago del producto comprado"""

    template_name = "perfiles/comprador/compras/crearDatosPago.html"
    model = datosPago
    form_class = DatosPagoForm
    success_url = reverse_lazy("misCompras")

    def dispatch(self, request, *args, **kwargs):
        logeado = self.request.user
        if self.request.user.is_authenticated:
            if (
                RegistroVenta.objects.filter(id=self.kwargs["pk"])
                .filter(usuario=logeado)
                .exists()
                or RegistroVenta.objects.filter(id=self.kwargs["pk"])
                .filter(product__author=logeado)
                .exists()
            ):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Acción invalida")
        else:
            return redirect(reverse_lazy("HomeIndexTemplateView"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Factura - Datos pago"
        return context

    def form_valid(self, form):
        miVenta = RegistroVenta.objects.get(id=self.kwargs["pk"])
        form.instance.venta = miVenta
        with transaction.atomic():
            form.save()
            estado_nuevo = EstadoOperacion.objects.get(nombre="Confirmando pago")
            RegistroVenta.objects.filter(id=self.kwargs["pk"]).update(
                estado_operacion=estado_nuevo
            )
            if self.request.user.groups.get().name == "Vendedor":
                return redirect("/detalleVenta/" + str(miVenta.id))
            elif self.request.user.groups.get().name == "Comprador":
                return redirect("/detalleCompra/" + str(miVenta.id))


class UpdateDatosPagoUpdateView(LoginRequiredMixin, UpdateView):  # Validado
    """Vista encargada de editar o actualizar los datos de pago del producto comprado"""

    template_name = "perfiles/comprador/compras/crearDatosPago.html"
    model = datosPago
    form_class = DatosPagoForm
    success_url = reverse_lazy("HomePerfilTemplateView")

    def get_object(self, queryset=None):
        logeado = self.request.user

        if (
            RegistroVenta.objects.filter(id=self.kwargs["pk"])
            .filter(usuario=logeado)
            .exists()
            or RegistroVenta.objects.filter(id=self.kwargs["pk"])
            .filter(product__author=logeado)
            .exists()
        ):
            return datosPago.objects.get(venta__id=self.kwargs["pk"])
        else:
            raise Http404("Venta no existe")

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("Venta no existe")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Factura - Datos pago"
        return context

    def form_valid(self, form):
        venta = RegistroVenta.objects.get(id=self.kwargs["pk"])
        if form.is_valid():
            form.save()
            if self.request.user.groups.get().name == "Vendedor":
                return redirect("/detalleVenta/" + str(venta.id))
            elif self.request.user.groups.get().name == "Comprador":
                return redirect("/detalleCompra/" + str(venta.id))


# Vendedor - vistas Ventas


class MisVentasActivasListView(LoginRequiredMixin, validarGrupo, ListView):
    """Vista encargada de mostrar la lista de ventas que aun siguen activas, es decir sin ser canceladas o haber sido entragadas"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = RegistroVenta
    template_name = "perfiles/vendedor/ventas/misVentas.html"
    paginate_by = 8

    def get_queryset(self):
        return RegistroVenta.objects.filter(
            product__author__pk=self.request.user.pk
        ).filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Ventas activas"
        context["letra"] = "Vendedor"
        return context


class MisVentasCerradasListView(LoginRequiredMixin, validarGrupo, ListView):
    """Vista encargada de mostrar la lista de ventas cerradas, es decir que fueron canceladas o sus productos fueron entregados"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    model = RegistroVenta
    template_name = "perfiles/vendedor/ventas/misVentas.html"

    def get_queryset(self):
        return RegistroVenta.objects.filter(
            product__author__pk=self.request.user.pk
        ).filter(state=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Ventas cerradas"
        context["letra"] = "Vendedor"
        return context


class DetalleVentaUpdateView(LoginRequiredMixin, validarGrupo, UpdateView):
    """Vista encargada de mostrar la factura o detalles de la venta y ofrece la opción de cambiar el estado de la venta"""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name = "perfiles/vendedor/ventas/detalleVenta.html"
    model = RegistroVenta
    form_class = EstadoOperacionForm
    success_url = reverse_lazy("MisVentasActivasListView")

    def get_object(self, queryset=None):
        return (
            RegistroVenta.objects.filter(product__author=self.request.user)
            .filter(state=True)
            .get(id=self.kwargs["pk"])
        )

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("Venta no existe")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Venta - " + self.get_object().product.name
        if datosPago.objects.filter(venta__id=self.kwargs["pk"]).exists():
            datos_Pago = datosPago.objects.get(venta__id=self.kwargs["pk"])
            context["datosPago"] = datos_Pago
        else:
            context["datosPago"] = "Indefinido"

        if datosEnvio.objects.filter(venta__id=self.kwargs["pk"]).exists():
            datos = datosEnvio.objects.get(venta__id=self.kwargs["pk"])
            context["datosEnvio"] = datos
        else:
            context["datosEnvio"] = "Indefinido"
        return context

    def form_valid(self, form):
        if (
            form.instance.estado_operacion.nombre == "Entregado"
            or form.instance.estado_operacion.nombre == "Cancelado"
        ):
            form.instance.state = False
        return super().form_valid(form)


class DetalleVentaCerradaTemplateView(
    LoginRequiredMixin, validarGrupo, TemplateView
):  # Validado
    """Vista encargada de mostrar el detalle de la venta o factura cuando esta tiene un status de cerrada."""

    grupo = "Vendedor"
    url_redirect = reverse_lazy("HomePerfilTemplateView")
    template_name = "perfiles/vendedor/ventas/detalleVentaCerrada.html"
    success_url = reverse_lazy("MisVentasActivasListView")

    def dispatch(self, request, *args, **kwargs):
        try:
            venta = RegistroVenta.objects.filter(product__author=self.request.user).get(
                id=self.kwargs["pk"]
            )
            if not venta.state:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("/detalleVenta/" + str(self.kwargs["pk"]))
        except ObjectDoesNotExist:
            raise Http404("Venta no econtrada")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        venta = RegistroVenta.objects.filter(product__author=self.request.user).get(
            id=self.kwargs["pk"]
        )
        if datosPago.objects.filter(venta__id=self.kwargs["pk"]).exists():
            datos_Pago = datosPago.objects.get(venta__id=self.kwargs["pk"])
            context["datosPago"] = datos_Pago
        else:
            context["datosPago"] = "Indefinido"

        if datosEnvio.objects.filter(venta__id=self.kwargs["pk"]).exists():
            datos = datosEnvio.objects.get(venta__id=self.kwargs["pk"])
            context["datosEnvio"] = datos
        else:
            context["datosEnvio"] = "Indefinido"

        context["title"] = "Venta - " + venta.product.name
        context["venta"] = venta
        return context
