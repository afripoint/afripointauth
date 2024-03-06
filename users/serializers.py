from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapters import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from django_countries.serializers_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    gender = serializers.CharField(source="profile.gender")
    phone = PhoneNumberField(source="profile.phone")
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


class CustomUserSerializer(RegisterSerializer):
    username = None
    phone = PhoneNumberField(required=True)
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data["username"] = self.cleaned_data["email"]
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        return user
