from rest_framework import serializers


class PhoneNumberValidationSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True)


class PhoneNumberVerificationSerializer(serializers.Serializer):
    otp = serializers.CharField(required=True)
    phone_number = serializers.CharField(required=True)
