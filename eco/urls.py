from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.inventario.urls')),
    path('', include('apps.venta.urls')),
    path('', include('apps.perfiles.urls')),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()