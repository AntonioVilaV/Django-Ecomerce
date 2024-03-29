from django.urls import path

from apps.sale.views import (
    BuyProductCreateView,
    ClosedSalesDetailTemplateView,
    MyActivePurchasesListView,
    MyActiveSalesListView,
    MyClosedSalesListView,
    MyPurchasesClosedListView,
    PaymentDetailsCreateView,
    PaymentDetailsUpdateView,
    PurchaseDetailView,
    SaleDetailsUpdateView,
    ShippingDetailsCreateView,
    ShippingDetailsUpdateView,
)

urlpatterns = [
    path(
        "buy/<int:pk>/",
        BuyProductCreateView.as_view(),
        name="BuyProductCreateView",
    ),
    path(
        "my_purchases/active/",
        MyActivePurchasesListView.as_view(),
        name="MyActivePurchasesListView",
    ),
    path(
        "my_purchases/closed/",
        MyPurchasesClosedListView.as_view(),
        name="MyPurchasesClosedListView",
    ),
    path(
        "purchase_detail/<int:pk>/",
        PurchaseDetailView.as_view(),
        name="PurchaseDetailView",
    ),
    path(
        "shipping_details/<int:pk>/",
        ShippingDetailsCreateView.as_view(),
        name="ShippingDetailsCreateView",
    ),
    path(
        "update_shipping_details/<int:pk>/",
        ShippingDetailsUpdateView.as_view(),
        name="ShippingDetailsUpdateView",
    ),
    path(
        "payment_details/<int:pk>/",
        PaymentDetailsCreateView.as_view(),
        name="PaymentDetailsCreateView",
    ),
    path(
        "update_payment_details/<int:pk>/",
        PaymentDetailsUpdateView.as_view(),
        name="PaymentDetailsUpdateView",
    ),
    path(
        "my_sales/active/",
        MyActiveSalesListView.as_view(),
        name="MyActiveSalesListView",
    ),
    path(
        "my_sales/closed/",
        MyClosedSalesListView.as_view(),
        name="MyClosedSalesListView",
    ),
    path(
        "sale_detail/<int:pk>/",
        SaleDetailsUpdateView.as_view(),
        name="SaleDetailsUpdateView",
    ),
    path(
        "closed_sales_detail/<int:pk>/",
        ClosedSalesDetailTemplateView.as_view(),
        name="ClosedSalesDetailTemplateView",
    ),
]
