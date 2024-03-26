from datetime import datetime, timedelta
import random
from django.conf import settings
from rest_framework import serializers
from direct7 import Client
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.utils import setup_user_email
from allauth.account import app_settings as allauth_settings
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from OTP.models import MFATable
from utils.utils import infobip_send_sms
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from utils.utils import UniqueOtpGenerator

client = Client(api_token=settings.D7_NETWORK_SECRET_KEY)
User = get_user_model()

otp_generator = UniqueOtpGenerator()


def getOTPInfo(self, phone_number):
    otp_info = client.verify.send_otp(
        originator="SignOTP",
        recipient=phone_number,
        content="Your OTP code is: {}",
        expiry=120,
        data_coding="text",
    )
    return otp_info


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=settings.MIN_PASSWORD_LENGTH,
        error_messages={
            "min_length": "Password must be longer than {} characters".format(
                settings.MIN_PASSWORD_LENGTH
            )
        },
    )

    class Meta:
        model = User
        fields = ("id", "phone_number", "email", "password1", "password2")
        read_only_fields = ("id",)

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data


class OTPRegisterSerializer(RegisterSerializer):
    # username = None
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    dob = serializers.DateTimeField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "phone_number": self.validated_data.get("phone_number"),
            "email": self.validated_data.get("email"),
            "first_name": self.validated_data.get("first_name"),
            "last_name": self.validated_data.get("last_name"),
            "dob": self.validated_data.get("dob"),
            "password1": self.validated_data.get("password1"),
            "password2": self.validated_data.get("password2"),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self, commit=False)
        user.phone_number = self.cleaned_data["phone_number"]
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.dob = self.cleaned_data["dob"]
        user.is_active = True
        user.save()

        try:
            adapter.clean_password(self.cleaned_data["password1"], user=user)

        except ValidationError as e:
            raise serializers.ValidationError(detail=serializers.as_serializer_error(e))

        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user


class CustomLoginSerializer(serializers.Serializer):
    login = serializers.CharField()
    password = serializers.CharField(style={"input_type": "password"})

    def validate(self, attrs):
        login = attrs.get("login")
        password = attrs.get("password")
        user = None

        user = authenticate(
            request=self.context.get("request"), phone_number=login, password=password
        )

        if not user:
            try:
                validate_email(login)
                user = authenticate(
                    request=self.context.get("request"), email=login, password=password
                )
            except ValidationError:
                pass

        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise AuthenticationFailed(msg, "authorization")

        attrs["user"] = user
        return attrs
