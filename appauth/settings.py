from datetime import timedelta
from pathlib import Path
from decouple import config
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = (config("SECRET_KEY"),)

DEBUG = True

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # custom
    "pages",
    "applogger",
    # external
    "allauth",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_yasg",
    "common",
    "kyc",
    "users",
    "corsheaders",
    "OTP",
    "customaccounts",
    "django_rest_passwordreset",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "appauth.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "appauth.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


DATABASES = {
    "default": {
        "ENGINE": config("ENGINE"),
        "USER": config("DB_USER"),
        "NAME": config("DB_NAME"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    },
}


# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "USER": "postgres",
#         "NAME": "afriauthdb",
#         "PASSWORD": "afripoint",
#         "HOST": "localhost",
#         "PORT": 5432,
#     },
# }

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

STATIC_URL = "/static/"

MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


EMAIL_BACKEND = str(config("EMAIL_BACKEND"))
EMAIL_HOST = str(config("EMAIL_HOST"))
EMAIL_PORT = str(config("EMAIL_PORT"))
EMAIL_HOST_USER = str(config("EMAIL_HOST_USER"))
DEFAULT_FROM_EMAIL = str(config("DEFAULT_FROM_EMAIL"))
EMAIL_HOST_PASSWORD = str(config("MAIL_HOST_PASSWORD"))
EMAIL_USE_TLS = str(config("EMAIL_USE_TLS"))


AUTH_USER_MODEL = "users.CustomUser"

MAX_OTP_TRY = 3


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
    ),
    # "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_FILTER_BACKENDS": ("django_filters.rest_framework.DjangoFilterBackend",),
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer", "JWT"),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": config("SIGNING_KEY"),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.token.AccessToken"),
}


SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "SIGNING_KEY": config("SIGNING_KEY"),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
}

REST_AUTH = {
    "USE_JWT": True,
    "JWT_AUTH_COOKIE": "appauth-token",
    "JWT_AUTH_REFRESH_COOKIE": "appauth-refresh-token",
    "REGISTER_SERIALIZER": "users.serializers.OTPRegisterSerializer",
    "LOGIN_SERIALIZER": "users.serializers.CustomLoginSerializer",
    # "PASSWORD_CHANGE_SERIALIZER": "rest-auth/password/change/",
}

AUTHENTICATION_BACKENDS = [
    "users.backend.CustomAuthenticationBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 1
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_NOTIFICATIONS = False
ACCOUNT_UNIQUE_EMAIL = True


MIN_PASSWORD_LENGTH = 3

D7_NETWORK_SECRET_KEY = str(config("D7_NETWORK_SECRET_KEY"))


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(name)-12s %(asctime)s %(module)s "
            "%(process)d %(thread)d %(message)s"
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "verbose",
        },
        "mail_admins": {
            "level": "ERROR",
            "class": "django.utils.log.AdminEmailHandler",
            "formatter": "verbose",
        },
        # "db": {
        #     "level": "WARNING",
        #     "class": "applogger.log_handler.DbLogHandler",
        # },
        # "activitity": {
        #     "level": "WARNING",
        #     "class": "customaccounts.activity_log_handler.AccountActivityLogHandler",
        # },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "mail_admins"],
            "level": "INFO",
            "propagate": True,
        },
    },
    "root": {
        "handlers": ["console", "mail_admins"],
        "level": "INFO",
    },
}

SWAGGER_SETTINGS = {
    "DEFAULT_FIELD_INSPECTORS": [
        "drf_yasg.inspectors.CamelCaseJSONFilter",
        "drf_yasg.inspectors.InlineSerializerInspector",
        "drf_yasg.inspectors.RelatedFieldInspector",
        "drf_yasg.inspectors.ChoiceFieldInspector",
        "drf_yasg.inspectors.FileFieldInspector",
        "drf_yasg.inspectors.DictFieldInspector",
        "drf_yasg.inspectors.SimpleFieldInspector",
        "drf_yasg.inspectors.StringDefaultFieldInspector",
    ],
}


JAZZMIN_SETTINGS = {
    "site_title": "Afripoint Auth Admin",
    "site_header": "Afripoint Auth Admin",
    "site_brand": "Afripoint AuthAdmin",
    "site_logo": "images/logo.png",
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "sidebar": "sidebar-light-warning",
    "welcome_sign": "Afripoint Auth",
    "copyright": "Afripoint Auth",
    "search_model": "auth.User",
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Home", "url": "admin:index", "permissions": ["auth.view_user"]},
        {"model": "auth.User"},
        {"app": ""},
    ],
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": ["django_summernote"],
    "hide_models": [],
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
}
