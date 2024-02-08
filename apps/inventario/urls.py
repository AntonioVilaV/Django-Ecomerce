from django.urls import path
from django.conf import settings

from apps.inventario.views import ActionPublicacionTemplateView, BuscarProductoListView, CrearPublicacionCreateView, EliminarPublicacionDeleteView,ProductoDetailView, ListaPublicacionesVendedorActivasListView, ListaPublicacionesVendedorPausadasListView, UpdatePublicacionUpdateView

from django.conf.urls.static import static

urlpatterns = [
    path('publicaciones/activas/',ListaPublicacionesVendedorActivasListView.as_view(),name="ListaPublicacionesVendedorActivasListView"),
    path('publicaciones/pausadas/',ListaPublicacionesVendedorPausadasListView.as_view(),name="ListaPublicacionesVendedorPausadasListView"),
    path('publicacion/add/',CrearPublicacionCreateView.as_view(),name="CrearPublicacionCreateView"),
    path('publicacion/update/<int:pk>/',UpdatePublicacionUpdateView.as_view(),name="UpdatePublicacionUpdateView"),
    path('publicacion/delete/<int:pk>/',EliminarPublicacionDeleteView.as_view(),name="EliminarPublicacionDeleteView"),
    path('producto/action/<str:action>/<int:pk>/',ActionPublicacionTemplateView.as_view(),name="ActionPublicacionTemplateView"),
    path('producto/<int:pk>/',ProductoDetailView.as_view(),name="ProductoDetailView"),
    
    
    path('buscar/',BuscarProductoListView.as_view(),name="BuscarProductoListView"),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)