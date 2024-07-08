from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AirtimeConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "creditswitch.bills"
    verbose_name = _("CreditSwitch Bills")
