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
    dob = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    createdAt = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    # def _str_(self):
    #     return self.email
