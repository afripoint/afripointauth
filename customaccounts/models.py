from django.db import models
import uuid
from django.contrib.auth import get_user_model
from common.models import TimeStampedModel
from kyc.models import KYCModel

User = get_user_model()


class AccountName(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


def get_default_account_name():
    return AccountName.objects.get_or_create(name="wallet")[0]


class AccountTypeTable(TimeStampedModel):
    accountTypeId = models.CharField(max_length=25, unique=True, blank=True, null=True)
    accountTypeName = models.OneToOneField(
        AccountName, on_delete=models.CASCADE, default=get_default_account_name
    )
    descriptions = models.TextField(max_length=255, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.accountTypeName.name

    class Meta:
        verbose_name = "AccountTypeTable"
        verbose_name_plural = "AccountTypeTables"


class AccountTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountNo = models.CharField(max_length=25, blank=True, null=True)
    accountName = models.CharField(max_length=100, blank=True, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=50, blank=True, null=True)
    accountTypeId = models.ForeignKey(
        AccountTypeTable, on_delete=models.CASCADE, blank=True, null=True
    )
    kycId = models.ForeignKey(KYCModel, on_delete=models.CASCADE, blank=True, null=True)
    kycStatus = models.BooleanField(default=False)
    createdBy = models.CharField(max_length=25, blank=True, null=True)
    dateCreated = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=25, blank=True, null=True)
    dateModified = models.DateField(auto_now=True)
    approvedBy = models.CharField(max_length=25, blank=True, null=True)
    approvedDate = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.userId.get_full_name


class AccountActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountNo = models.CharField(max_length=25, blank=True, null=True)
    accountName = models.CharField(max_length=100, blank=True, null=True)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    activityType = models.CharField(max_length=50, blank=True, null=True)
    userId = models.CharField(max_length=255, blank=True, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.dateCreated} - {self.activityType}"

    class Meta:
        ordering = ["-dateCreated"]



