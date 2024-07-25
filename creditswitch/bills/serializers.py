# serializers.py
from rest_framework import serializers

from creditswitch.bills.models import (
    CreditSwitchAirTimeService,
    CreditSwitchDataService,
    CreditSwitchEletricityService,
    CreditSwitchShowmaxService,
)


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


class ShowMaxPaySerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=10)
    subscriptionType = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, coerce_to_string=False
    )
    customerNo = serializers.CharField(max_length=15)
    invoicePeriod = serializers.CharField(max_length=15)
    packageName = serializers.CharField(max_length=15)


class ServiceIdSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=10)


class MultichoiceValidateCustomerSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=15)
    customer_no = serializers.CharField(max_length=25)


class ElectricityValidateRequestSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=15)
    customer_account_id = serializers.CharField(max_length=25)


class ElectricityPurchaseSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=15)
    customer_account_id = serializers.CharField(max_length=25)
    amount = serializers.CharField(max_length=25)
    customer_name = serializers.CharField(max_length=25)
    customer_address = serializers.CharField(max_length=25)


class MultichoicePurchaseSerializer(serializers.Serializer):
    service_id = serializers.CharField(max_length=15)
    customer_no = serializers.CharField(max_length=25)
    amount = serializers.CharField(max_length=25)
    customer_name = serializers.CharField(max_length=25)
    products_codes = serializers.CharField(max_length=25)
    invoice_period = serializers.CharField(max_length=25)


class CreditSwitchAirTimeServiceSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField(read_only=True)
    code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CreditSwitchAirTimeService
        fields = ["provider", "code"]

    def get_provider(self, obj):
        provider = obj.provider
        return provider

    def get_code(self, obj):
        code = obj.code
        return code


class CreditSwitchDataServiceSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField(read_only=True)
    code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CreditSwitchDataService
        fields = ["provider", "code"]

    def get_provider(self, obj):
        provider = obj.provider
        return provider

    def get_code(self, obj):
        code = obj.code
        return code


class CreditSwitchEletricitySerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField(read_only=True)
    code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CreditSwitchEletricityService
        fields = ["provider", "code"]

    def get_provider(self, obj):
        provider = obj.provider
        return provider

    def get_code(self, obj):
        code = obj.code
        return code


class CreditSwitchShowmaxSerializer(serializers.ModelSerializer):
    provider = serializers.SerializerMethodField(read_only=True)
    code = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = CreditSwitchShowmaxService
        fields = ["provider", "code"]

    def get_provider(self, obj):
        provider = obj.provider
        return provider

    def get_code(self, obj):
        code = obj.code
        return code
