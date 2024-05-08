from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
import uuid


User = get_user_model()

from common.models import TimeStampedModel

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
)

STATUS = (
    ("verified", "Verified"),
    ("unverified", "Unverified"),
)


class KYCModel(TimeStampedModel):
    account_no = models.CharField(
        _("Account No"), max_length=255, blank=True, null=True
    )
    user = models.OneToOneField(User, related_name="kyc", on_delete=models.CASCADE)
    bvn = models.CharField(_("BVN"), blank=True, null=True, unique=True, max_length=15)
    nin = models.CharField(_("NIN"), blank=True, null=True, unique=True, max_length=15)
    # user_id = models.GeneratedField(
    #     output_field=models.CharField(), expression=models.F("user_id"), db_persist=True
    # )
    status = models.CharField(
        max_length=11,
        choices=STATUS,
        blank=True,
        null=True,
        unique=True,
        default="unverified",
    )

    def __str__(self):
        return f"{self.user.get_full_name } KYC"

    class Meta:
        verbose_name = "KYC"
        verbose_name_plural = "KYC"
        ordering = ["-dateCreated"]
