import logging
from django.db.models.signals import post_save, post_migrate
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from appauth.settings import AUTH_USER_MODEL
from kyc.models import KYCModel

User = get_user_model()

from .models import (
    AccountName,
    AccountTable,
    AccountTypeTable,
    get_default_account_name,
)

logger = logging.getLogger(__name__)


@receiver(post_migrate)
def create_default_account_name(sender, **kwargs):
    if sender.name == "customaccounts":
        get_default_account_name()


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_account_type(sender, instance, created, **kwargs):
    if created:
        kyc = KYCModel.objects.get(user=instance)
        acct_name, _ = AccountName.objects.get_or_create(name="wallet")
        acct_type, _ = AccountTypeTable.objects.get_or_create(accountTypeName=acct_name)
        AccountTable.objects.create(userId=instance, kycId=kyc, accountTypeId=acct_type)
