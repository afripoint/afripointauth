from rest_framework import serializers

from accounts.models import AccountName, AccountTypeTable


class AccountTypeSerializer(serializers.ModelSerializer):
    accountTypeName = serializers.SlugRelatedField(
        slug_field="name", queryset=AccountName.objects.all()
    )

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
