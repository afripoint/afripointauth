from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountName(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name


def get_default_account_name():
    # This function tries to get an AccountName instance with a specific name
    # If it doesn't exist, it creates it and returns it
    account_name, created = AccountName.objects.get_or_create(name="wallet")
    return account_name.pk


class AccountTypeTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountTypeId = models.CharField(
        max_length=25, unique=True, blank=True, null=True
    )  # What will be the nature of this field
    accountTypeName = models.ForeignKey(
        AccountName, on_delete=models.CASCADE, default=get_default_account_name
    )
    descriptions = models.TextField(max_length=255, blank=True, null=True)
    createdBy = models.CharField(max_length=25, blank=True, null=True)
    dateCreated = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=25, blank=True, null=True)
    dateModified = models.DateField(auto_now=True)
    approvedBy = models.CharField(max_length=25, blank=True, null=True)
    approvedDate = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.accountTypeName.name


class Kyc(models.Model):
    pass


class AccountTable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountNo = models.CharField(max_length=25)
    accountName = models.CharField(max_length=100, blank=True, null=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=50, blank=True, null=True)
    accountTypeId = models.ForeignKey(AccountTypeTable, on_delete=models.CASCADE)
    kycId = models.ForeignKey(Kyc, on_delete=models.CASCADE)
    kycStatus = models.BooleanField()
    createdBy = models.CharField(max_length=25, blank=True, null=True)
    dateCreated = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=25, blank=True, null=True)
    dateModified = models.DateField(auto_now=True)
    approvedBy = models.CharField(max_length=25, blank=True, null=True)
    approvedDate = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.accountName


class AccountActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountNo = models.CharField(max_length=25, blank=True, null=True)
    accountName = models.CharField(max_length=100, blank=True, null=True)
    activityType = models.CharField(max_length=50, blank=True, null=True)
    userId = models.CharField(
        max_length=25, blank=True, null=True
    )  # This should be a foreign key to the user
    dateCreated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.accountNo} - {self.activityType}"
