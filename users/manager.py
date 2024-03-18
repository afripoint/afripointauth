from django.contrib.auth.models import (
    BaseUserManager,
)
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone=None, password=None, **extra_fields):
        """
        Create and return a regular user with an email (if provided) and password.
        """
        if not email and not phone:
            raise ValueError(_("Email or Phone is required"))
        if email:
            email = self.normalize_email(email)
            user = self.model(email=email, **extra_fields)
        else:
            user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone, password=None, **extra_fields):
        """
        Create and return a superuser with an email (not phone) and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        user = self.create_user(email, phone, password, **extra_fields)
        user.save(using=self._db)

        return user
