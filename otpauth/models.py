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
    otp = models.CharField(max_length=20, blank=True, null=True)

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
