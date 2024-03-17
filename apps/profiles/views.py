from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models import Q
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from apps.inventory.models import Product
from apps.profiles.forms import (
    ContactDetailsForm,
    UserDetailsForm,
    UserRegistrationForm,
)
from apps.profiles.models import ContactDetails
from apps.sale.models import SalesRecord

# Create your views here.


class HomeIndexTemplateView(TemplateView):
    """Root view of the platform, showing the different categories and promotions."""

    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["man"] = Product.objects.filter(status=True).filter(
            category__name="Men"
        )[:8]
        context["kids"] = Product.objects.filter(status=True).filter(
            category__name="Childrens"
        )[:8]
        context["women"] = Product.objects.filter(status=True).filter(
            category__name="Women"
        )[:8]

        context["title"] = "Eshop Django"
        return context


# Seller - Vistas


class ProfileHomeTemplateView(LoginRequiredMixin, TemplateView):
    """Home view of the user profile, in charge of displaying the status of the Seller's sale and purchase transactions."""

    template_name = "profiles/home_user.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Home"

        if self.request.user.groups.get().name == "Seller":
            active_sales = (
                SalesRecord.objects.filter(product__author=self.request.user)
                .filter(state=True)
                .count()
            )
            payments_to_be_confirmed = (
                SalesRecord.objects.filter(product__author__pk=self.request.user.pk)
                .filter(
                    Q(operating_status__name="Waiting for payment")
                    | Q(operating_status__name="Confirming payment")
                )
                .count()
            )
            products_to_be_shipped = (
                SalesRecord.objects.filter(product__author__pk=self.request.user.pk)
                .filter(operating_status__name="Processing order")
                .count()
            )
            context["resumen"] = [
                active_sales,
                payments_to_be_confirmed,
                products_to_be_shipped,
            ]
        elif self.request.user.groups.get().name == "Buyer":
            purchases = (
                SalesRecord.objects.filter(user=self.request.user.pk)
                .filter(state=True)
                .count()
            )
            invoices = (
                SalesRecord.objects.filter(user=self.request.user.pk)
                .filter(operating_status__name="Waiting for payment")
                .count()
            )
            shipments = (
                SalesRecord.objects.filter(user=self.request.user.pk)
                .filter(
                    Q(operating_status__name="Processing order")
                    | Q(operating_status__name="Sent to")
                )
                .count()
            )
            context["resumen"] = [purchases, invoices, shipments]
        return context


# Buyer - Vistas


class MyAccountUpdateView(LoginRequiredMixin, UpdateView):
    """View in charge of displaying my account data and gives the option to upgrade"""

    model = ContactDetails
    second_model = User
    template_name = "profiles/my_account.html"
    form_class = ContactDetailsForm
    second_form_class = UserDetailsForm
    success_url = reverse_lazy("ProfileHomeTemplateView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - My account"
        user = self.second_model.objects.get(id=self.kwargs["pk"])

        if "form" not in context:
            context["form"] = self.form_class()
        if "form2" not in context:
            context["form2"] = self.second_form_class(instance=user)
        return context

    def get_object(self, queryset=None):
        logeado = self.request.user
        datos = ContactDetails.objects.get(user__id=self.kwargs["pk"])
        if datos.user == logeado:
            return datos
        else:
            raise Http404("Access denied")

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            return super().dispatch(request, *args, **kwargs)
        except ContactDetails.DoesNotExist:
            raise Http404("Data not exists")

    def post(self, request, *args, **kwargs):
        if self.object.user == self.request.user:
            form_user_data = UserDetailsForm(request.POST, instance=self.request.user)
            form_contact_data = ContactDetailsForm(request.POST, instance=self.object)

            if form_user_data.is_valid() and form_contact_data.is_valid():
                form_user_data.save(commit=False)
                form_contact_data.save()
                form_user_data.save()
                return self.render_to_response(self.get_context_data())
            else:
                return self.render_to_response(
                    self.get_context_data(form=form_contact_data, form2=form_user_data)
                )
        else:
            raise Http404("Access denied")


class UserRegistrationCreateView(CreateView):
    """View in charge of registering a user in the platform database"""

    model = User
    template_name = "profiles/register.html"
    form_class = UserRegistrationForm
    success_url = reverse_lazy("ProfileHomeTemplateView")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Register"
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(reverse_lazy("ProfileHomeTemplateView"))
        else:
            return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        response = super().form_valid(form)
        group_id = self.request.POST["groups"]
        group = Group.objects.get(id=group_id)
        with transaction.atomic():
            group.user_set.add(self.object)
            ContactDetails.objects.create(user=self.object)
        new_user = authenticate(
            username=form.cleaned_data.get("username"),
            password=form.cleaned_data.get("password1"),
        )
        login(self.request, new_user)

        return response


# Session Vistas


class LoginUserLoginView(LoginView):
    """View in charge of displaying login form"""

    template_name = "log/log.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Login"
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("ProfileHomeTemplateView")
        return super().dispatch(request, *args, **kwargs)


class ContactDetailsTemplateView(TemplateView):
    """This view is responsible for displaying a user's contact details and verifying whether you have permissions to view them."""

    template_name = "profiles/contacto/contact_details.html"

    def dispatch(self, request, *args, **kwargs):
        if (
            SalesRecord.objects.filter(user=self.request.user)
            .filter(product__author__id=self.kwargs["pk"])
            .exists()
            or SalesRecord.objects.filter(user__id=self.kwargs["pk"])
            .filter(product__author=self.request.user)
            .exists()
        ):
            return super().dispatch(request, *args, **kwargs)
        else:
            raise Http404("Object not found")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Eshop Django - Contact details"

        context["contacto"] = ContactDetails.objects.get(id=self.kwargs["pk"])
        return context
