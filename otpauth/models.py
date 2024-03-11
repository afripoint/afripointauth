from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from otpauth.manager import CustomUserManager

phone_number_validator = RegexValidator(
    regex=r"^\d{11}$", message="Phone number must be 11 digits."
)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(
        unique=True, max_length=11, validators=[phone_number_validator]
    )
    email = models.EmailField(unique=True, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"

    def _str_(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff
