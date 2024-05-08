from rest_framework import serializers

from kyc.models import KYCModel
from users.serializers import UserSerializer


class KYCSerializer(serializers.ModelSerializer):
    user_id = serializers.CharField(source="user.id", required=False)
    user = UserSerializer(read_only=True)

    class Meta:
        model = KYCModel
        fields = ["bvn", "nin", "status", "account_no", "user_id", "user"]
