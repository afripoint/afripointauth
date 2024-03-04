from django.contrib.auth.models import (
    BaseUserManager,
)


class CustomUserManagerWithPhoneOnly(BaseUserManager):
    def create_user(self, password=None, phone=None, **extra_fields):
        """
        Create and return a regular user with an email (if provided) and password.
        """
        if not phone:
            raise ValueError(_("Users must have a phone number"))
        else:
            user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with an email (not phone) and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))

        return self.create_user(email, password, **extra_fields)
