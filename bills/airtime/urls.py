from django.urls import include, path
from .views import PurchaseAirtimeView, airtime_vend_request, buyairtime

urlpatterns = [
    path("", airtime_vend_request, name="airtime-vend-request"),
    path("buyairtime/", buyairtime, name="buyairtime"),
    path("purchase-airtime/", PurchaseAirtimeView.as_view(), name="purchase-airtime"),
]
