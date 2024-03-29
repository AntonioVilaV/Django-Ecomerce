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

from apps.inventory.forms import CreateProductForm, InventoryForm, UpdateProductForm
from apps.inventory.models import Inventory, Product
from mixins import ValidateGroup


# Seller - Vistas Products
class ActivePublicationsListView(LoginRequiredMixin, ValidateGroup, ListView):
    """View in charge of displaying the list of Publications or published products that are active. View for user type Seller"""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    model = Product
    template_name = "profiles/seller/publications/publications.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Active publications"
        return context

    def get_queryset(self):
        return Product.objects.filter(status=True).filter(author=self.request.user)


class PausedPublicationsListView(LoginRequiredMixin, ValidateGroup, ListView):
    """View in charge of showing the list of Publications or published products that are paused. View for user type Seller"""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    model = Product
    template_name = "profiles/seller/publications/publications.html"
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Paused publications"
        return context

    def get_queryset(self):
        return Product.objects.filter(author=self.request.user).filter(status=False)


class PublicationCreateView(LoginRequiredMixin, ValidateGroup, CreateView):
    """View in charge of creating product or publication to sell on the platform"""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    template_name = "profiles/seller/publications/createPublication.html"
    model = Product
    form_class = CreateProductForm
    second_form_class = InventoryForm
    success_url = reverse_lazy("ProfileHomeTemplateView")

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
            inventory = form2.save(commit=False)
            form.instance.author = self.request.user
            form.instance.status = True
            if "photo" in self.request.FILES:
                form.instance.photo = self.request.FILES["photo"]
            inventory.product = form.save()
            inventory.save()

            return redirect(reverse_lazy("ActivePublicationsListView"))
        else:
            return self.render_to_response(
                self.get_context_data(form=form, form2=form2)
            )


class PublicationUpdateView(LoginRequiredMixin, ValidateGroup, UpdateView):
    """View in charge of updating or editing the data of a Product"""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    template_name = "profiles/seller/publications/updatePublication.html"
    model = Product
    second_model = Inventory
    form_class = UpdateProductForm
    second_form_class = InventoryForm

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Product not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Update publication"

        product = self.model.objects.get(id=self.kwargs["pk"])
        inventory = self.second_model.objects.get(product=product)

        if "form" not in context:
            context["form"] = self.form_class(instance=product)
        if "form2" not in context:
            context["form2"] = self.second_form_class(instance=inventory)
        return context

    def post(self, request, *args, **kwargs):
        if self.model.objects.filter(id=self.kwargs["pk"]).filter(
            author=self.request.user
        ):
            product = self.model.objects.get(id=self.kwargs["pk"])
            quantity = self.second_model.objects.get(product=product)
            form = self.form_class(request.POST, instance=product)
            form2 = self.second_form_class(request.POST, instance=quantity)

            if form.is_valid() and form2.is_valid():
                if "photo" in self.request.FILES:
                    form.instance.photo = self.request.FILES["photo"]
                form.save()
                form2.save()

                if form.instance.status:
                    self.success_url = reverse_lazy("ActivePublicationsListView")
                else:
                    self.success_url = reverse_lazy("PausedPublicationsListView")

                return redirect(self.get_success_url())
            else:
                return self.render_to_response(
                    self.get_context_data(form=form, form2=form2)
                )
        else:
            raise Http404("Action denied")


class PublicationDeleteView(LoginRequiredMixin, ValidateGroup, DeleteView):
    """View in charge of deleting product or publication"""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    model = Product
    template_name = "profiles/seller/publications/deletePublication.html"
    success_url = reverse_lazy("ActivePublicationsListView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Delete publication"
        return context

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author == self.request.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Product not found")

    def post(self, request, *args, **kwargs):
        if self.object.author == self.request.user:
            self.object.delete()
            return redirect(reverse_lazy("ActivePublicationsListView"))
        else:
            raise Http404("Action denied")


class ActionPublicationTemplateView(LoginRequiredMixin, ValidateGroup, TemplateView):
    """View in charge of managing and executing actions on publications; Activate or pause publication."""

    grupo = "Seller"
    url_redirect = reverse_lazy("ProfileHomeTemplateView")
    template_name = "profiles/seller/publications/actionPublication.html"

    def dispatch(self, request, *args, **kwargs):
        try:
            product = Product.objects.filter(author=self.request.user).get(
                id=self.kwargs["pk"]
            )
            if self.kwargs["action"] == "pause" and product.status:
                return super().dispatch(request, *args, **kwargs)
            elif self.kwargs["action"] == "activate" and not product.status:
                return super().dispatch(request, *args, **kwargs)
            else:
                raise Http404("Incorrect action")
        except Product.DoesNotExist:
            raise Http404("Product not found")

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
        context["product"] = Product.objects.get(id=self.kwargs["pk"])
        return context

    def post(self, request, *args, **kwargs):
        product = Product.objects.filter(id=self.kwargs["pk"])
        if self.request.user == product.get().author:
            if self.kwargs["action"] == "activate":
                if "quantity" in request.POST:
                    quantity = request.POST["quantity"]
                    if quantity.isdigit() and int(quantity) > 0:
                        with transaction.atomic():
                            Inventory.objects.filter(product=product.get()).update(
                                quantity=quantity
                            )
                            product.update(status=True)
                            return redirect(reverse_lazy("ActivePublicationsListView"))
                    else:
                        return self.render_to_response(
                            self.get_context_data(
                                error="The quantity must be a number greater than 0 in order to activate the publication."
                            )
                        )
            elif self.kwargs["action"] == "pause":
                product.update(status=False)
                return redirect(reverse_lazy("PausedPublicationsListView"))


# Buyer - Vistas products
class ProductDetailView(DetailView):
    """View in charge of displaying product details to the buyer and giving options and purchase details"""

    model = Product
    template_name = "profiles/buyer/publications/productDetail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(id=self.kwargs["pk"])
        context["title"] = product.name
        context["product"] = product
        return context


class ProductSearchListView(ListView):
    """View in charge of showing the list of products resulting from the search in the upper input of the template (grid of products filtered by the search engine)."""

    model = Product
    template_name = "profiles/buyer/publications/shop-grid.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - " + self.request.GET["search"]
        context["new_products"] = Product.objects.filter(status=True).order_by(
            "-created"
        )[:4]
        return context

    def get_queryset(self):
        search = self.request.GET["search"]

        try:
            category = self.request.GET.getlist("categories")[0]
        except IndexError:
            category = "categories"

        if category == "categories":
            return Product.objects.filter(name__icontains=search).filter(status=True)
        elif category == "decV":
            return Product.objects.filter(status=True).filter(discount__discount__gte=0)
        else:
            return (
                Product.objects.filter(category__name=category)
                .filter(status=True)
                .filter(name__icontains=search)
            )
