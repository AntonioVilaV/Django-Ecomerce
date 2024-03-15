from django.conf.urls import include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("apps.inventory.urls")),
    path("", include("apps.sale.urls")),
    path("", include("apps.perfiles.urls")),
]
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
