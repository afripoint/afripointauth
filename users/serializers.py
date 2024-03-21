from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from django.core.exceptions import ValidationError
from users.models import CustomUser

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender")
    first_name = serializers.CharField(source="profile.first_name")
    last_name = serializers.CharField(source="profile.last_name")
    picture = serializers.ReadOnlyField(source="profile.picture.url")
    country = CountryField(source="profile.country")
    city = serializers.CharField(source="profile.city")

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "phone",
            "gender",
            "first_name",
            "last_name",
            "phone",
            "gender",
            "country",
            "city",
            "picture",
        ]

    def to_representation(self, instance):
        representation = super(UserSerializer, self).to_representation(instance)
        if instance.is_superuser:
            representation["is_admin"] = True
        return representation


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ("id", "phone", "email", "password")

    def validate(self, data):
        email = data.get("email")
        phone = data.get("phone")

        if not email and not phone:
            raise ValidationError("An email address or phone number must be provided.")
        if email and phone:
            raise ValidationError(
                "Please provide only one contact method: email or phone."
            )

        return data

    def create(self, validated_data):
        # Remove password from validated_data to handle it separately
        password = validated_data.pop("password", None)

        if validated_data.get("email"):
            # Create a user instance with an email
            user = CustomUser.objects.create(**validated_data)
        elif validated_data.get("phone"):
            # Create a user instance with a phone
            user = CustomUser.objects.create(**validated_data)

        # Setting the user's password using set_password to handle hashing
        if password:
            user.set_password(password)
            user.save()

        return user
