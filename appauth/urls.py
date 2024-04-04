from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static

from otpauth.views import CustomUserDetailsView
from rest_framework.routers import DefaultRouter

from OTP.views import (
    PhoneNumberValidationView,
    PhoneNumberVerificationView,
    EmailValidationView,
    EmailVerificationView,
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
    path("accounts/", include("allauth.urls")),
    path("api/v1/auth/", include("dj_rest_auth.urls")),
    path("api/v1/auth/registration/", include("dj_rest_auth.registration.urls")),
    path("api/v1/auth/user/", CustomUserDetailsView.as_view(), name="user_details"),
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
    path("otp/", include(router.urls)),
]

# urlpatterns += router.urls

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Afripoint Authentication"
admin.site.site_title = "Afripoint Authentication Portal"
admin.site.index_title = "Welcome to Afripoint Authentication Portal"
