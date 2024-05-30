from rest_framework import serializers

from users.serializers import UserSerializer
from .models import (
    TransactionLog,
    TransactionDetails,
    TransactionLog,
    Transaction,
)


# class TransactionStatusSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TransactionStatus
#         fields = ["status_id", "status_name", "status_description"]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "transaction_id",
            "user_id",
            "transaction_type",
            "amount",
            "payment_method",
            "transaction_status",
            "timestamp",
            "error_message",
            "additional_details",
        ]


class TransactionLogSerializer(serializers.ModelSerializer):
    user_id = UserSerializer(read_only=True)

    class Meta:
        model = TransactionLog
        fields = [
            "transaction_id",
            "user_id",
            "transaction_type",
            "amount",
            "payment_method",
            "transaction_status",
            "timestamp",
            "error_message",
            "additional_details",
        ]


class TransactionDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionDetails
        fields = [
            "transaction",
            "vendor_id",
            "account_id",
            "invoice_id",
            "transaction_description",
            "transaction_reference",
        ]


# class TransactionLogSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TransactionLog
#         fields = [
#             "transaction_id",
#             "user_id",
#             "transaction_type",
#             "amount",
#             "payment_method",
#             "transaction_status",
#             "timestamp",
#             "error_message",
#             "additional_details",
#         ]
