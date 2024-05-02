from django.apps import AppConfig


class custom_accountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "customaccounts"

    def ready(self):
        from customaccounts import signals
