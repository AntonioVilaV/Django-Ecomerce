from django.contrib import admin
from django.urls import path
from django.conf.urls import include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('inventario.urls')),
    path('', include('venta.urls')),
    path('', include('perfiles.urls')),
]
#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()