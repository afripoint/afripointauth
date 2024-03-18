from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

from common.models import TimeStampedModel

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
)


class KYCModel(TimeStampedModel):
    user = models.OneToOneField(User, related_name="kyc", on_delete=models.CASCADE)
    bvn = models.PositiveIntegerField(_("BVN"), blank=True, null=True, unique=True)
    nin = models.PositiveIntegerField(_("NIN"), blank=True, null=True, unique=True)

    def __str__(self):
        return f"{self.user.email }'s KYC"

    class Meta:
        verbose_name = "KYC"
        verbose_name_plural = "KYC"
        ordering = ["-createdAt"]
