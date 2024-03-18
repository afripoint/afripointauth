from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

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
            "gender",
            "first_name",
            "last_name",
            "phone",
            "gender",
            "country",
            "city",
            "picture",
        ]

    def to_repreaentation(self, instance):
        representation = super().to_representation(instance)
        if instance.is_superuser:
            representation["admin"] = True
        return representation


class CreateUserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["id", "email", "phone", "password"]
