from datetime import timedelta
from pathlib import Path
from decouple import config
from os import getenv, path
from decouple import config

# import cloudinary
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ["*"]

DJANGO_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "allauth",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth.account",
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "drf_yasg",
    "corsheaders",
    "django_rest_passwordreset",
    "import_export",
    # "djcelery_email",
    # "django_celery_beat",
]

LOCAL_APPS = [
    "pages",
    "applogger",
    "common",
    "kyc",
    "users",
    "OTP",
    "customaccounts",
    "transactions",
    "creditswitch.bills",
    "dojah",
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

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
        "DIRS": [path.join(BASE_DIR, "templates")],
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

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL")


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT", 5432),
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

STATIC_URL = "/static/"

MEDIA_ROOT = path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

STATIC_ROOT = path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    path.join(BASE_DIR, "static"),
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

# D7_NETWORK_SECRET_KEY = str(config("D7_NETWORK_SECRET_KEY"))


DOJAH_SECRET_KEY = config("DOJAH_SECRET_KEY")
DOJAH_APP_ID = config("DOJAH_APP_ID")


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

CSRF_TRUSTED_ORIGINS = [
    "https://backend.onenairapay.com",
]

# settings.py

# SECURE_SSL_REDIRECT = True  # Redirect all non-HTTPS requests to HTTPS
# SECURE_HSTS_SECONDS = 3600  # HTTP Strict Transport Security (HSTS)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


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

# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Creditswitch
LOGIN_ID = config("LOGIN_ID")
PUBLIC_KEY = config("PUBLIC_KEY")
PRIVATE_KEY = config("PRIVATE_KEY")
