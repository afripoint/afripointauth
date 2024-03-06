import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from appauth.settings import AUTH_USER_MODEL

from kyc.models import KYCModel

logger = logging.getLogger(__name__)


@receiver(post_save, sender=AUTH_USER_MODEL)
def create_user_kyc(sender, instance, created, **kwargs):
    if created:
        KYCModel.objects.create(user=instance)
        logger.info(f"{instance}'s kcy created")


# @receiver(post_save, sender=AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     logger.info(f"{instance}'s profile created")
