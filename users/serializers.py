from rest_framework import serializers
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
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from utils.utils import UniqueOtpGenerator
from datetime import datetime, timedelta


User = get_user_model()

otp_generator = UniqueOtpGenerator()


def get_mfa(userId):
    mfa = MFATable.objects.filter(userId=userId).order_by("-date_generated").first()
    return mfa


class UserSerializer(serializers.ModelSerializer):
    # render_class = [SingleUserJSONRenderer]

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "phone_number",
        ]

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class OTPRegisterSerializer(RegisterSerializer):
    # username = None
    email = serializers.EmailField(required=False)
    phone_number = serializers.CharField(required=False)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    dob = serializers.DateField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    registration_type = serializers.CharField(write_only=True)

    def registration_type_check(self, registration_type, userId):
        mfa = get_mfa(userId)

        # Check if an MFA record exists and if it's verified.
        if mfa is None or not mfa.verified:
            raise serializers.ValidationError(f"{userId} is not verified")

    def validate_dob(self, value):
        """
        Validate that the user is 18 years old or above.
        """
        today = datetime.now().date()
        age_limit = today - timedelta(days=365 * 18)

        if value > age_limit:
            raise ValidationError("Must be 18 years or older to register.")

        return value

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "phone_number": self.validated_data.get("phone_number"),
            "email": self.validated_data.get("email"),
            "first_name": self.validated_data.get("first_name"),
            "last_name": self.validated_data.get("last_name"),
            "dob": self.validated_data.get("dob"),
            "registration_type": self.validated_data["registration_type"],
            "password1": self.validated_data.get("password1"),
            "password2": self.validated_data.get("password2"),
        }

    def save(self, request):
        adapter = get_adapter()
        self.cleaned_data = self.get_cleaned_data()
        phone_number = self.cleaned_data["phone_number"]
        registration_type = self.cleaned_data["registration_type"]
        email = self.cleaned_data["email"]

        # Perform the phone number state check early in the process.
        # This will raise a ValidationError if the phone number is not verified, preventing further execution.

        if registration_type == "mobile":
            self.registration_type_check(registration_type, phone_number)

        if registration_type == "web":
            self.registration_type_check(registration_type, email)

        # Assuming phone_number_state_check raises an exception if verification fails,
        # the following code only runs if verification succeeds.
        user = adapter.new_user(request)
        user.phone_number = phone_number
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.dob = self.cleaned_data["dob"]
        user.is_active = True  # Set the user as active because OTP is verified

        # Remove the commit=False to ensure user is saved only after passing the verification.
        adapter.save_user(request, user, self)

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
            request=self.context.get("request"), username=login, password=password
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
