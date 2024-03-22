from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.views import PasswordResetConfirmView

# from users.views import CustomUserDetailView
# from users.views import UserViewSet
from rest_framework.routers import DefaultRouter

from otpauth.views import OTPVerificationView


# from users.views import CustomUserDetailView


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
# router.register("user-otp", UserViewSet, basename="user-otp"),
# router.register("verify/", OTPVerificationView, basename="verify")


urlpatterns = [
    path("backoffice/", admin.site.urls),
    path("accounts/", include("allauth.urls")),
    # path("api/v1/auth/user/", CustomUserDetailView.as_view(), name="user_details"),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path(
        "api/v1/auth/password/reset/confirm/<uidb64>/<token>/",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
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
]

urlpatterns += router.urls

admin.site.site_header = "Afripoint Authentication"
admin.site.site_title = "Afripoint Authentication Portal"
admin.site.index_title = "Welcome to Afripoint Authentication Portal"
