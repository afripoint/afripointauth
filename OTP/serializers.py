from rest_framework import serializers


# Phone Serializers
class PhoneNumberValidationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class PhoneNumberVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)


# Email Serializers
class EmailValidationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
