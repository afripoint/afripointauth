from rest_framework import serializers
from django.contrib.auth import get_user_model

from customaccounts.models import (
    AccountActivity,
    AccountName,
    AccountTable,
    AccountTypeTable,
)
from kyc.models import KYCModel
from kyc.serializers import KYCSerializer
from users.serializers import UserSerializer

User = get_user_model()


# class UserSerializer(serializers.ModelSerializer):
#     full_name = serializers.CharField(source="get_full_name", read_only=True)

#     class Meta:
#         model = User
#         fields = ("id", "full_name", "email")


class AccountTypeSerializer(serializers.ModelSerializer):
    accountTypeName = serializers.SlugRelatedField(
        slug_field="name", queryset=AccountName.objects.all()
    )

    createdBy = UserSerializer(read_only=True)

    class Meta:
        model = AccountTypeTable
        fields = [
            "accountTypeName",
            "descriptions",
            "createdBy",
            "modifiedBy",
            "approvedBy",
            "approvedDate",
            "active",
        ]

    def validate_accountTypeName(self, value):
        """
        Check if the accountTypeName already exists in the database.
        """
        if AccountTypeTable.objects.filter(accountTypeName=value).exists():
            raise serializers.ValidationError("This account type already exist.")
        return value

    def create(self, validated_data):
        validated_data["createdBy"] = self.context["request"].user
        validated_data["modifiedBy"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update the modifier and optionally the approver
        instance.modifiedBy = self.context["request"].user
        if "approvedBy" in validated_data:
            instance.approvedBy = self.context["request"].user
        return super().update(instance, validated_data)


class AccountTableSerialzer(serializers.ModelSerializer):
    accountTypeId = serializers.SlugRelatedField(
        slug_field="accountTypeId", queryset=AccountTypeTable.objects.all()
    )

    createdBy = UserSerializer(read_only=True)
    userId = UserSerializer(read_only=True)
    kycId = KYCSerializer(read_only=True)

    class Meta:
        model = AccountTable
        fields = [
            "accountNo",
            "accountName",
            "accountTypeId",
            "userId",
            "kycId",
            "createdBy",
            "modifiedBy",
            "approvedBy",
            "approvedDate",
            "active",
        ]

    def validate_accountTypeId(self, value):
        if AccountTable.objects.filter(accountTypeId=value).exists():
            raise serializers.ValidationError(
                "This user already have this account type"
            )
        return value

    def create(self, validated_data):
        validated_data["createdBy"] = self.context["request"].user

        validated_data["modifiedBy"] = self.context["request"].user
        if "approvedBy" in validated_data:
            validated_data["approvedBy"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance.modifiedBy = self.context["request"].user
        if "approvedBy" in validated_data:
            instance.modifiedBy = self.context["request"].user
        return super().update(instance, validated_data)


class AccountActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountActivity
        fields = [
            "id",
            "accountNo",
            "accountName",
            "ip_address",
            "user_agent",
            "activityType",
            "userId",
            "dateCreated",
        ]
