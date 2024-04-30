from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from users.manager import CustomUserManager
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    phone_number = models.CharField(unique=True, max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    otp = models.CharField(max_length=20, blank=True, null=True)
    user_source = models.CharField(max_length=20, blank=True, null=True)
    mobile_country_code = models.CharField(max_length=4, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # createdAt = models.DateTimeField(auto_now_add=True)
    createdBy = models.CharField(max_length=25, blank=True, null=True)
    dateCreated = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=25, blank=True, null=True)
    dateModified = models.DateField(auto_now=True)
    approvedBy = models.CharField(max_length=25, blank=True, null=True)
    approvedDate = models.DateField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"

    @property
    def get_full_name(self):
        # Use the first_name and last_name if available, otherwise return email or a placeholder
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email or self.phone_number

    def clean(self):
        today = timezone.now().date()
        age_limit = today - timedelta(days=365 * 18)

        if self.dob and self.dob >= age_limit:
            raise ValidationError("Date of birth must be at least 18 years.")

    def save(self, *args, **kwargs):
        self.full_clean()  # Call the clean method to validate the data
        super().save(*args, **kwargs)
