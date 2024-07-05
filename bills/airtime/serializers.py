# serializers.py
from rest_framework import serializers


class PurchaseAirtimeSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=10)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    recipient = serializers.CharField(max_length=15)


class PurchaseDataSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=10)
    product_id = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    recipient = serializers.CharField(max_length=15)


class PurchaseDataSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=10)
    product_id = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    recipient = serializers.CharField(max_length=15)


class ServiceIdSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=10)
