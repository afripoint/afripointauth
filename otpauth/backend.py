from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q


User = get_user_model()


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        users = User.objects.filter(
            Q(email__iexact=username) | Q(phone_number__iexact=username)
        )
        for user in users:
            if user.check_password(password):
                return user
        return None


# class EmailOrPhoneBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             # Check if username is an email
#             validate_email(username)
#             kwargs = {"email": username}
#         except ValidationError:
#             # If not an email, treat as a phone number
#             kwargs = {"phone_number": username}

#         if kwargs:
#             try:
#                 user = User.objects.get(**kwargs)
#                 if user.check_password(password):
#                     return user
#             except User.DoesNotExist:
#                 pass
#         return None
