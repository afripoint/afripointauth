from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from otpauth.manager import CustomUserManager
from django.conf import settings

# phone_number_validator = RegexValidator(
#     regex=r"^\d{11}$", message="Phone number must be 11 digits."
# )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(unique=True, max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    otp_max_out = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"

    def _str_(self):
        return self.email if self.email else self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


class OTPUpdate(models.Model):
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    otp_code = models.CharField(max_length=255, blank=True, null=True)
    otp_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.phone_number
