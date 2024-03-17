from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, TemplateView, UpdateView

from apps.inventory.models import Inventory, Product
from apps.sale.forms import (
    OperatingStatusForm,
    PaymentForm,
    SalesForm,
    ShippingDataForm,
)
from apps.sale.models import (
    OperatingStatus,
    PaymentDetails,
    SalesRecord,
    ShippingDetails,
)
from mixins import ValidateGroup

# Create your views here.


# Buyer - Vista Ventas
class BuyProductCreateView(LoginRequiredMixin, ValidateGroup, CreateView):
    """Vista encargada de mandar la peticion de compra de producto y crear la venta en la base de datos"""

    grupo = "Buyer"
    url_redirect = reverse_lazy("LoginUserLoginView")
    models = SalesRecord
    template_name = "profiles/buyer/shopping/confirm_purchase.html"
    form_class = SalesForm
    success_url = "/comprar/CompraRealizada/"

    def dispatch(self, request, *args, **kwargs):
        try:
            Product.objects.get(id=self.kwargs["pk"])
        except Product.DoesNotExist:
            raise Http404("Product not found")

        if not Product.objects.get(id=self.kwargs["pk"]).status:
            raise Http404("Product disabled")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs["pk"])
        context["title"] = "Comprar - " + product.name
        context["product"] = product
        return context

    def form_valid(self, form):
        pro = Product.objects.get(id=self.kwargs["pk"])
        qty = 1
        if "quant[1]" in self.request.POST:
            qty = int(self.request.POST["quant[1]"])

            if qty > int(pro.inventory_product.quantity):
                return self.render_to_response(
                    self.get_context_data(
                        quantity_error="Out of stock, please enter a smaller quantity"
                    )
                )  # especificar que debe pedir una quantity menor de productos

        with transaction.atomic():
            form.instance.user = self.request.user
            form.instance.product = pro
            discount = 0

            if pro.get_discount():
                form.instance.discount = int(pro.discount.discount)
                discount = (int(pro.price) * qty) * (int(pro.discount.discount) / 100)
            form.instance.quantity = qty
            form.instance.total = (qty * pro.price) - discount
            form.instance.operating_status = OperatingStatus.objects.get(id=1)
            self.object = form.save()

            inv = Inventory.objects.get(product=pro)
            inv.quantity -= qty
            inv.save()

            if inv.quantity == 0:
                pro.status = False
                pro.save()
            return redirect(reverse_lazy("MyActivePurchasesListView"))


class MyActivePurchasesListView(LoginRequiredMixin, ValidateGroup, ListView):
    """View in charge of displaying a list of the user's active purchases. Purchases that do not have status delivered or cancelled."""

    grupo = "Buyer"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    model = SalesRecord
    template_name = "profiles/buyer/shopping/my_purchases.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Active purchases"
        return context

    def get_queryset(self):
        return SalesRecord.objects.filter(user=self.request.user.pk).filter(state=True)


class MyPurchasesClosedListView(LoginRequiredMixin, ValidateGroup, ListView):
    """View in charge of displaying a list of the user's closed purchases. Purchases with status delivered or cancelled"""

    grupo = "Buyer"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    model = SalesRecord
    template_name = "profiles/buyer/shopping/my_purchases.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Closed purchases"
        return context

    def get_queryset(self):
        return SalesRecord.objects.filter(user=self.request.user.pk).filter(state=False)


class PurchaseDetailView(LoginRequiredMixin, TemplateView):
    """View in charge of displaying purchase details or purchase invoice to the user"""

    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    template_name = "profiles/buyer/shopping/purchase_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            sale = SalesRecord.objects.filter(user=self.request.user).get(
                id=self.kwargs["pk"]
            )
        except SalesRecord.DoesNotExist:
            raise Http404("Sale not exist")

        if PaymentDetails.objects.filter(sale__id=sale.id).exists():
            context["payment_details"] = PaymentDetails.objects.get(sale__id=sale.id)
        else:
            context["payment_details"] = "Undefined"

        if ShippingDetails.objects.filter(sale__id=sale.id).exists():
            context["shipping_details"] = ShippingDetails.objects.get(sale__id=sale.id)
        else:
            context["shipping_details"] = "Undefined"
        context["title"] = "Buy - " + sale.product.name
        context["sale"] = sale
        return context


class ShippingDetailsCreateView(LoginRequiredMixin, CreateView):
    """View in charge of creating the buyer's shipping data"""

    template_name = "profiles/buyer/shopping/shipping_details.html"
    model = ShippingDetails
    form_class = ShippingDataForm
    success_url = reverse_lazy("MyActiveSalesListView")

    def dispatch(self, request, *args, **kwargs):
        logged = self.request.user
        if logged.is_authenticated:
            if (
                SalesRecord.objects.filter(id=self.kwargs["pk"])
                .filter(user=logged)
                .exists()
                or SalesRecord.objects.filter(id=self.kwargs["pk"])
                .filter(product__author=logged)
                .exists()
            ):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Sale does not exist")
        else:
            return redirect(reverse_lazy("HomeIndexTemplateView"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoice - Shipping details"
        return context

    def form_valid(self, form):
        my_sale = SalesRecord.objects.get(id=self.kwargs["pk"])
        form.instance.sale = my_sale

        if form.is_valid():
            form.save()
            if self.request.user.groups.get().name == "Seller":
                return redirect("/sale_detail/" + str(my_sale.id))
            elif self.request.user.groups.get().name == "Buyer":
                return redirect("/purchase_detail/" + str(my_sale.id))


class ShippingDetailsUpdateView(LoginRequiredMixin, UpdateView):
    """View in charge of editing or updating the buyer's shipping data in the purchase made."""

    template_name = "profiles/buyer/shopping/update_shipping_details.html"
    model = ShippingDetails
    form_class = ShippingDataForm
    success_url = reverse_lazy("ProfileHomeTemplateView")

    def get_object(self, queryset=None):
        logged = self.request.user
        if (
            SalesRecord.objects.filter(id=self.kwargs["pk"])
            .filter(user=logged)
            .exists()
            or SalesRecord.objects.filter(id=self.kwargs["pk"])
            .filter(product__author=logged)
            .exists()
        ):
            return ShippingDetails.objects.get(sale__id=self.kwargs["pk"])

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("Data do not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoice - Shipping details"
        return context

    def form_valid(self, form):
        sale = SalesRecord.objects.get(id=self.kwargs["pk"])
        if form.is_valid():
            form.save()
            if self.request.user.groups.get().name == "Seller":
                return redirect("/sale_detail/" + str(sale.id))
            elif self.request.user.groups.get().name == "Buyer":
                return redirect("/purchase_detail/" + str(sale.id))


class PaymentDetailsCreateView(LoginRequiredMixin, CreateView):
    """View in charge of adding receipts and payment data for the purchased product"""

    template_name = "profiles/buyer/shopping/payment_date.html"
    model = PaymentDetails
    form_class = PaymentForm
    success_url = reverse_lazy("misCompras")

    def dispatch(self, request, *args, **kwargs):
        logged = self.request.user
        if self.request.user.is_authenticated:
            if (
                SalesRecord.objects.filter(id=self.kwargs["pk"])
                .filter(user=logged)
                .exists()
                or SalesRecord.objects.filter(id=self.kwargs["pk"])
                .filter(product__author=logged)
                .exists()
            ):
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Invalid action")
        else:
            return redirect(reverse_lazy("HomeIndexTemplateView"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoice - Payment details"
        return context

    def form_valid(self, form):
        my_sale = SalesRecord.objects.get(id=self.kwargs["pk"])
        form.instance.sale = my_sale
        with transaction.atomic():
            form.save()
            estado_nuevo = OperatingStatus.objects.get(name="Confirming payment")
            SalesRecord.objects.filter(id=self.kwargs["pk"]).update(
                operating_status=estado_nuevo
            )
            if self.request.user.groups.get().name == "Seller":
                return redirect("/sale_detail/" + str(my_sale.id))
            elif self.request.user.groups.get().name == "Buyer":
                return redirect("/purchase_detail/" + str(my_sale.id))


class PaymentDetailsUpdateView(LoginRequiredMixin, UpdateView):  # Validado
    """View in charge of editing or updating the payment details of the product purchased"""

    template_name = "profiles/buyer/shopping/payment_date.html"
    model = PaymentDetails
    form_class = PaymentForm
    success_url = reverse_lazy("ProfileHomeTemplateView")

    def get_object(self, queryset=None):
        logged = self.request.user

        if (
            SalesRecord.objects.filter(id=self.kwargs["pk"])
            .filter(user=logged)
            .exists()
            or SalesRecord.objects.filter(id=self.kwargs["pk"])
            .filter(product__author=logged)
            .exists()
        ):
            return PaymentDetails.objects.get(sale__id=self.kwargs["pk"])
        else:
            raise Http404("Sale does not exist")

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("Sale does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Invoice - Payment details"
        return context

    def form_valid(self, form):
        sale = SalesRecord.objects.get(id=self.kwargs["pk"])
        if form.is_valid():
            form.save()
            if self.request.user.groups.get().name == "Seller":
                return redirect("/sale_detail/" + str(sale.id))
            elif self.request.user.groups.get().name == "Buyer":
                return redirect("/purchase_detail/" + str(sale.id))


# Seller - vistas Ventas


class MyActiveSalesListView(LoginRequiredMixin, ValidateGroup, ListView):
    """View in charge of displaying the list of sales that are still active, i.e. not yet cancelled or delivered."""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    model = SalesRecord
    template_name = "profiles/seller/sales/my_sales.html"
    paginate_by = 8

    def get_queryset(self):
        return SalesRecord.objects.filter(
            product__author__pk=self.request.user.pk
        ).filter(state=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Active sales"
        return context


class MyClosedSalesListView(LoginRequiredMixin, ValidateGroup, ListView):
    """View in charge of displaying the list of closed sales, i.e. that were cancelled or their products were delivered."""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    model = SalesRecord
    template_name = "profiles/seller/sales/my_sales.html"

    def get_queryset(self):
        return SalesRecord.objects.filter(
            product__author__pk=self.request.user.pk
        ).filter(state=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Closed sales"
        return context


class SaleDetailsUpdateView(LoginRequiredMixin, ValidateGroup, UpdateView):
    """View in charge of displaying the invoice or sale details and offers the option to change the status of the sale."""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    template_name = "profiles/seller/sales/sale_details.html"
    model = SalesRecord
    form_class = OperatingStatusForm
    success_url = reverse_lazy("MyActiveSalesListView")

    def get_object(self, queryset=None):
        return (
            SalesRecord.objects.filter(product__author=self.request.user)
            .filter(state=True)
            .get(id=self.kwargs["pk"])
        )

    def dispatch(self, request, *args, **kwargs):
        try:
            return super().dispatch(request, *args, **kwargs)
        except ObjectDoesNotExist:
            raise Http404("sale does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Sale - " + self.get_object().product.name
        if PaymentDetails.objects.filter(sale__id=self.kwargs["pk"]).exists():
            datos_Pago = PaymentDetails.objects.get(sale__id=self.kwargs["pk"])
            context["payment_details"] = datos_Pago
        else:
            context["payment_details"] = "Undefined"

        if ShippingDetails.objects.filter(sale__id=self.kwargs["pk"]).exists():
            datos = ShippingDetails.objects.get(sale__id=self.kwargs["pk"])
            context["shipping_details"] = datos
        else:
            context["shipping_details"] = "Undefined"
        return context

    def form_valid(self, form):
        if (
            form.instance.operating_status.name == "Entregado"
            or form.instance.operating_status.name == "Cancelado"
        ):
            form.instance.state = False
        return super().form_valid(form)


class ClosedSalesDetailTemplateView(LoginRequiredMixin, ValidateGroup, TemplateView):
    """View in charge of showing the detail of the sale or invoice when it has a closed status."""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    template_name = "profiles/seller/sales/closed_sales_detail.html"
    success_url = reverse_lazy("MyActiveSalesListView")

    def dispatch(self, request, *args, **kwargs):
        try:
            sale = SalesRecord.objects.filter(product__author=self.request.user).get(
                id=self.kwargs["pk"]
            )
            if not sale.state:
                return super().dispatch(request, *args, **kwargs)
            else:
                return redirect("/sale_detail/" + str(self.kwargs["pk"]))
        except ObjectDoesNotExist:
            raise Http404("Sale not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sale = SalesRecord.objects.filter(product__author=self.request.user).get(
            id=self.kwargs["pk"]
        )
        if PaymentDetails.objects.filter(sale__id=self.kwargs["pk"]).exists():
            datos_Pago = PaymentDetails.objects.get(sale__id=self.kwargs["pk"])
            context["payment_details"] = datos_Pago
        else:
            context["payment_details"] = "Undefined"

        if ShippingDetails.objects.filter(sale__id=self.kwargs["pk"]).exists():
            datos = ShippingDetails.objects.get(sale__id=self.kwargs["pk"])
            context["shipping_details"] = datos
        else:
            context["shipping_details"] = "Undefined"

        context["title"] = "Sale - " + sale.product.name
        context["sale"] = sale
        return context
