from datetime import datetime, timedelta
import random
from django.conf import settings
from rest_framework import serializers
from direct7 import client
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer.

    Used in POST and GET
    """

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
        """
        Validates if both password are same or not.
        """

        if data["password1"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data

    def create(self, validated_data):
        """
        Create method.

        Used to create the user
        """
        otp = random.randint(1000, 9999)
        otp_expiry = datetime.now() + timedelta(minutes=10)

        user = User(
            phone_number=validated_data["phone_number"],
            email=validated_data["email"],
            otp=otp,
            otp_expiry=otp_expiry,
            max_otp_try=settings.MAX_OTP_TRY,
        )
        user.set_password(validated_data["password1"])
        user.save()
        otp_response = client.verify.send_otp(
            originator="SignOTP",
            recipient=validated_data["phone_number"],
            content="Your OTP code is: {}",
            expiry=120,
            data_coding="text",
        )
        otp_id = otp_response["otp_id"]
        print("otp_id", otp_id)
        return user
