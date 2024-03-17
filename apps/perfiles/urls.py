from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.perfiles.views import (
    ContactDetailsTemplateView,
    HomeIndexTemplateView,
    LoginUserLoginView,
    MyAccountUpdateView,
    ProfileHomeTemplateView,
    UserRegistrationCreateView,
)

urlpatterns = [
    path("", HomeIndexTemplateView.as_view(), name="HomeIndexTemplateView"),
    path("home/", ProfileHomeTemplateView.as_view(), name="ProfileHomeTemplateView"),
    path(
        "my_account/<int:pk>/",
        MyAccountUpdateView.as_view(),
        name="MyAccountUpdateView",
    ),
    path(
        "register/",
        UserRegistrationCreateView.as_view(),
        name="UserRegistrationCreateView",
    ),
    path("login/", LoginUserLoginView.as_view(), name="LoginUserLoginView"),
    path("salir/", LogoutView.as_view(), name="LogoutView"),
    path(
        "contact_details/<int:pk>/",
        ContactDetailsTemplateView.as_view(),
        name="ContactDetailsTemplateView",
    ),
]
