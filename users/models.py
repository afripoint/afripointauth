from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    Group,
    Permission,
)
from django.utils.translation import gettext_lazy as _
from users.manager import CustomUserManager
import uuid
from django.contrib.auth import get_user_model


class CustomUser(AbstractBaseUser, PermissionsMixin):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    email = models.EmailField(
        _("email address"), db_index=True, unique=True, null=True, blank=True
    )
    phone = models.CharField(_("phone number"), max_length=15, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
        related_name="custom_user_set",  # Changed related_name
        related_query_name="custom_user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_set",  # Changed related_name
        related_query_name="custom_user",
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    # def __str__(self):
    #     return self.email if self.email else self.phone
