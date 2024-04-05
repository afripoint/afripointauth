from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import CustomUser

from .forms import CustomUserCreationForm, CustomUserChangeForm


class UserAdmin(BaseUserAdmin):
    ordering = ["email"]
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        "pkid",  # Ensure your CustomUser model has this field or remove it if it doesn't
        "id",
        "email",
        "phone_number",
        "is_staff",
        "is_active",
    ]
    list_display_links = ["id", "email", "phone_number"]
    list_filter = [
        "email",
        "phone_number",
        "is_staff",
        "is_active",
    ]  # Assuming 'is_active' is a field in your model
    fieldsets = (
        (
            _("Login Credentials"),
            {
                "fields": (
                    "phone_number",
                    "password",
                ),
            },
        ),
        (
            _("Personal Information"),
            {
                "fields": (
                    "phone_number",
                ),  # Remove the duplicate 'email' field from here
            },
        ),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important Dates"),
            {
                "fields": ("last_login",),
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "phone_number",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )
    search_fields = ["email", "phone_number"]


admin.site.register(CustomUser)
