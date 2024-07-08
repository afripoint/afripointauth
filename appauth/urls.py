from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static

from customaccounts.views import (
    AccountActivityView,
    AccountDetail,
    AccountTypeDetail,
    AccountTypeViewSet,
    AccountView,
)
from kyc.views import KYCAPIView
from users.views import CustomUserAPIView
from rest_framework.routers import DefaultRouter, SimpleRouter

from OTP.views import (
    PhoneNumberValidationView,
    PhoneNumberVerificationView,
    EmailValidationView,
    EmailVerificationView,
)

from transactions.views import (
    TransactionList,
    TransactionDetail,
    TransactionLogList,
    TransactionLogDetail,
    TransactionDetailsList,
)

schema_view = get_schema_view(
    openapi.Info(
        title="Afripoint Authentication API",
        default_version="v1",
        description="Afripoint Authentication API",
        terms_of_service="",
        contact=openapi.Contact(email="contact@afripointgroup"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register("mobile", PhoneNumberValidationView, basename="send_otp")
router.register("mobile", PhoneNumberVerificationView, basename="verfiy_otp")
router.register("web", EmailValidationView, basename="send_otp")
router.register("web", EmailVerificationView, basename="verfiy_otp")

urlpatterns = [
    path("backoffice/", admin.site.urls),
    path("customaccounts/", include("allauth.urls")),
    path("api/", include("dj_rest_auth.urls")),
    path("bills/", include("creditswitch.bills.urls")),
    path("api/registration/", include("dj_rest_auth.registration.urls")),
    path("api/auth/user/", CustomUserAPIView.as_view(), name="user_details"),
    path("api/kyc/<str:user_id>", KYCAPIView.as_view(), name="kyc_api_view"),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path("api/", include(router.urls)),
    path("api/customaccounts/type", AccountTypeViewSet.as_view(), name="account_type"),
    path(
        "api/customaccounts/<int:pk>/type",
        AccountTypeDetail.as_view(),
        name="single_account_type",
    ),
    path("api/customaccounts/", AccountView.as_view(), name="account_type"),
    path(
        "api/customaccounts/<int:pk>",
        AccountDetail.as_view(),
        name="acount_detail",
    ),
    path(
        "api/account/activities/",
        AccountActivityView.as_view(),
        name="acount_activities",
    ),
    # path(
    #     "api/transaction-status/",
    #     TransactionStatusList.as_view(),
    #     name="transactionstatus-list",
    # ),
    # path(
    #     "api/transaction-status/<int:pk>/",
    #     TransactionStatusDetail.as_view(),
    #     name="transactionstatus-detail",
    # ),
    path("api/transactions/", TransactionList.as_view(), name="transaction-list"),
    path(
        "api/transactions/<int:pk>/",
        TransactionDetail.as_view(),
        name="transaction-detail",
    ),
    path(
        "api/transaction-logs/",
        TransactionLogList.as_view(),
        name="transactionlog-list",
    ),
    path(
        "api/transaction-logs/<int:pk>/",
        TransactionLogDetail.as_view(),
        name="transactionlog-detail",
    ),
    path(
        "api/transaction-details/",
        TransactionDetailsList.as_view(),
        name="transactiondetails-list",
    ),
]

# urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Afripoint Authentication"
admin.site.site_title = "Afripoint Authentication Portal"
admin.site.index_title = "Welcome to Afripoint Authentication Portal"
