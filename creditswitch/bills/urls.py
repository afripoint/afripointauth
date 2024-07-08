from django.urls import path
from .views import (
    CreditSwitchAirTimeServiceView,
    DataPlansView,
    PurchaseAirtimeView,
    PurchaseDataView,
    ShowmaxView,
    StartimeView,
    TransactionStatusView,
    MerchantDetailsView,
    ShowMaxPayView,
)

urlpatterns = [
    path("purchase-airtime/", PurchaseAirtimeView.as_view(), name="purchase-airtime"),
    path("merchant-details/", MerchantDetailsView.as_view(), name="merchant-details"),
    path(
        "airtime-services/",
        CreditSwitchAirTimeServiceView.as_view(),
        name="airtime-services",
    ),
    path(
        "transaction-status/",
        TransactionStatusView.as_view(),
        name="transaction-status",
    ),
    path("data-plans/", DataPlansView.as_view(), name="data-plans"),
    path("data-purchase/", PurchaseDataView.as_view(), name="data-purchase"),
    path("showmax-packages/", ShowmaxView.as_view(), name="showmax-packages"),
    path("startimes/", StartimeView.as_view(), name="startimes"),
    path("showmax-subscribe/", ShowMaxPayView.as_view(), name="showmax-subscribe"),
]
