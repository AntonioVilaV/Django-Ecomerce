from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apps.inventory.views import (
    ActionPublicationTemplateView,
    ActivePublicationsListView,
    PausedPublicationsListView,
    ProductDetailView,
    ProductSearchListView,
    PublicationCreateView,
    PublicationDeleteView,
    PublicationUpdateView,
)

urlpatterns = [
    path(
        "publications/active/",
        ActivePublicationsListView.as_view(),
        name="ActivePublicationsListView",
    ),
    path(
        "publications/paused/",
        PausedPublicationsListView.as_view(),
        name="PausedPublicationsListView",
    ),
    path(
        "publication/add/",
        PublicationCreateView.as_view(),
        name="PublicationCreateView",
    ),
    path(
        "publication/update/<int:pk>/",
        PublicationUpdateView.as_view(),
        name="PublicationUpdateView",
    ),
    path(
        "publication/delete/<int:pk>/",
        PublicationDeleteView.as_view(),
        name="PublicationDeleteView",
    ),
    path(
        "publication/action/<str:action>/<int:pk>/",
        ActionPublicationTemplateView.as_view(),
        name="ActionPublicationTemplateView",
    ),
    path("product/<int:pk>/", ProductDetailView.as_view(), name="ProductDetailView"),
    path("buscar/", ProductSearchListView.as_view(), name="ProductSearchListView"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
