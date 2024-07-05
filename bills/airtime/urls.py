from django.urls import path
from .views import DataPlansView, PurchaseAirtimeView, PurchaseDataView, ShowmaxView, StartimeView, TransactionStatusView, MerchantDetailsView

urlpatterns = [
    path("purchase-airtime/", PurchaseAirtimeView.as_view(), name="purchase-airtime"),
    path("merchant-details/", MerchantDetailsView.as_view(), name="merchant-details"),
    path("transaction-status/", TransactionStatusView.as_view(), name="transaction-status"),
    path("data-plans/", DataPlansView.as_view(), name="data-plans"),
    path("data-purchase/", PurchaseDataView.as_view(), name="data-purchase"),
    path("showmax-packages/", ShowmaxView.as_view(), name="showmax-packages"),
    path("startimes/", StartimeView.as_view(), name="startimes"),


    



    





    


]
