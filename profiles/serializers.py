from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email")
    phone = serializers.CharField(source="user.phone")
    full_name = serializers.SerializerMethodField(read_only=True)
    country = CountryField(name_only=True)

    class meta:
        model = Profile
        fields = [
            "id",
            "first_name",
            "last_name",
            "full_name",
            "email",
            "picture",
            "gender",
            "country",
            "phone",
            "address",
        ]

    def get_full_name(self, obj):
        first_name = obj.first_name.title()
        last_name = obj.last_name.title()
        return f"{first_name} {last_name}"

    def get_picture(self, obj):
        return obj.picture.url


class UpdateProfileSerializer(serializers.ModelSerializer):
    class meta:
        model = Profile
        fields = ["picture", "gender", "country", "city", "address", "state"]
