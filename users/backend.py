from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)

        user = None
        if "@" in username:
            user = UserModel.objects.filter(email__iexact=username).first()
        else:
            user = UserModel.objects.filter(phone__iexact=username).first()

        if user and user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
