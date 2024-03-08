from dj_rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from rest_framework import serializers
from django_countries.serializer_fields import CountryField
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import get_user_model

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


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super().get_cleaned_data()
        return {
            "email": self.validated_data.get("email", ""),
            "password1": self.validated_data.get("password1", ""),
            "password2": self.validated_data.get("password2", ""),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        user.save()

        setup_user_email(request, user, [])
        user.email = self.cleaned_data["email"]
        user.password = self.cleaned_data["password1"]
        return user
