from django.urls import path

from venta.views import ComprarProductoCreateView, CrearDatosEnvioCreateView, CrearDatosPagoCreateView, DetalleCompraDetailView, DetalleVentaUpdateView, DetalleVentaCerradaTemplateView, MisComprasActivasListView, MisComprasCerradasListView, MisVentasActivasListView, MisVentasCerradasListView, UpdateDatosEnvioUpdateView, UpdateDatosPagoUpdateView

urlpatterns = [
    path('comprar/<int:pk>/', ComprarProductoCreateView.as_view(),name="ComprarProductoCreateView"),
    path('misCompras/Activas/', MisComprasActivasListView.as_view(),name="MisComprasActivasListView"),
    path('misCompras/Cerradas/', MisComprasCerradasListView.as_view(),name="MisComprasCerradasListView"),
    path('detalleCompra/<int:pk>/', DetalleCompraDetailView.as_view(),name="DetalleCompraDetailView"),

    path('crearDatosEnvio/<int:pk>/', CrearDatosEnvioCreateView.as_view(),name="CrearDatosEnvioCreateView"),
    path('updateDatosEnvio/<int:pk>/', UpdateDatosEnvioUpdateView.as_view(),name="UpdateDatosEnvioUpdateView"),

    path('crearDatosPago/<int:pk>/', CrearDatosPagoCreateView.as_view(),name="CrearDatosPagoCreateView"),
    path('updateDatosPago/<int:pk>/', UpdateDatosPagoUpdateView.as_view(),name="UpdateDatosPagoUpdateView"),

    path('misVentas/Activas/', MisVentasActivasListView.as_view(),name="MisVentasActivasListView"),
    path('misVentas/Cerradas/', MisVentasCerradasListView.as_view(),name="MisVentasCerradasListView"),
    path('detalleVenta/<int:pk>/', DetalleVentaUpdateView.as_view(),name="DetalleVentaUpdateView"),
    path('detalleVentaCerrada/<int:pk>/', DetalleVentaCerradaTemplateView.as_view(),name="DetalleVentaCerradaTemplateView"),
    
]