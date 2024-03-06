from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


from common.models import TimeStampedModel

GENDER = (
    ("male", "Male"),
    ("female", "Female"),
)


class Profiles(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    first_name = models.CharField(
        _("First Name"), max_length=100, blank=True, null=True
    )
    last_name = models.CharField(_("Last Name"), max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True)
    gender = models.CharField(
        _("Gender"), choices=GENDER, blank=True, null=True, max_length=10
    )
    address = models.CharField(_("Address"), max_length=255, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    state = models.CharField(_("State"), max_length=255, blank=True, null=True)
    country = CountryField(
        verbose_name=_("country"), default="NG", blank=False, null=False
    )
    post_code = models.CharField(_("Post Code"), max_length=255, blank=True, null=True)
    picture = models.ImageField(upload_to="kyc/", blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} Profile"

    class Meta:
        verbose_name = "Profiles"
        verbose_name_plural = "Profiles"
        ordering = ["-createdAt"]
