from rest_framework import serializers


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)


class NINSerializer(serializers.Serializer):
    nin = serializers.CharField(max_length=15)


class BVNSerializer(serializers.Serializer):
    bvn = serializers.CharField(max_length=15)


class VitualNINSerializer(serializers.Serializer):
    vnin = serializers.CharField(max_length=30)


class BVNSerializer(serializers.Serializer):
    bvn = serializers.CharField(max_length=30)
