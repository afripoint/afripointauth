from django.db import models
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone


MFA_CATEGORY = (
    ("registration", "Registration"),
    ("login", "Login"),
    ("transaction", "Transaction"),
)

MFA_TYPE = (
    ("signup", "Sign Up"),
    ("login", "Login"),
    ("resetpassword", "Reset Password"),
    ("forgotpassword", "Forgot Password"),
)


class MFATable(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    mfa_code = models.CharField(max_length=255, blank=True, null=True)
    date_generated = models.DateTimeField(auto_now_add=True)
    mfa_duration = models.PositiveBigIntegerField(blank=True, null=True)
    mfa_category = models.CharField(
        max_length=25, choices=MFA_CATEGORY, blank=True, null=True
    )
    otp_expiry = models.DateTimeField(blank=True, null=True)
    expired = models.BooleanField(default=False)
    userId = models.CharField(max_length=255, blank=True, null=True)
    mfa_type = models.CharField(max_length=255, choices=MFA_TYPE, blank=True, null=True)

    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.userId}-{self.date_generated}-{self.mfa_code}"


class OTPSettings(models.Model):
    otp_live_time = models.PositiveBigIntegerField()
    max_otp_try = models.CharField(max_length=5)

    def __str__(self):
        return "OTP Settings"

    def save(self, *args, **kwargs):
        if not self.pk and OTPSettings.objects.exists():
            # If trying to create a new instance and an instance already exists, update the existing one
            existing = OTPSettings.objects.first()
            existing.otp_live_time = self.otp_live_time
            existing.max_otp_try = self.max_otp_try
            existing.save(update_fields=["otp_live_time", "max_otp_try"])
        else:
            # No instance exists yet, or this is updating an existing instance, proceed normally.
            super().save(*args, **kwargs)
