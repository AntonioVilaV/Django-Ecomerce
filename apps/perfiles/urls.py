from django.contrib.auth.views import LogoutView
from django.urls import path

from apps.perfiles.views import (
    DatosDeContactoTemplateView,
    HomeIndexTemplateView,
    HomePerfilTemplateView,
    LoginUserLoginView,
    MiCuentaUpdateView,
    RegistroUsuarioCreateView,
)

urlpatterns = [
    path("", HomeIndexTemplateView.as_view(), name="HomeIndexTemplateView"),
    path("home/", HomePerfilTemplateView.as_view(), name="HomePerfilTemplateView"),
    path("miCuenta/<int:pk>", MiCuentaUpdateView.as_view(), name="MiCuentaUpdateView"),
    path(
        "registrar/",
        RegistroUsuarioCreateView.as_view(),
        name="RegistroUsuarioCreateView",
    ),
    path("login/", LoginUserLoginView.as_view(), name="LoginUserLoginView"),
    path("salir/", LogoutView.as_view(), name="LogoutView"),
    path(
        "datosContacto/<int:pk>/",
        DatosDeContactoTemplateView.as_view(),
        name="DatosDeContactoTemplateView",
    ),
]
