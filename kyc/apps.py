from django.apps import AppConfig


class KycConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "kyc"

    def ready(self):
        from kyc import signals
