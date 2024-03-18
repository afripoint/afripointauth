import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Profiles

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_kyc(sender, instance, created, **kwargs):
    if created:
        Profiles.objects.create(user=instance)
        logger.info(f"{instance}'s Profile created")


# @receiver(post_save, sender=AUTH_USER_MODEL)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     logger.info(f"{instance}'s profile created")
