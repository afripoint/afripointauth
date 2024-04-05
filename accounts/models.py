from django.db import models
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


class AccountType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountTypeId = models.CharField(
        max_length=25, unique=True
    )  # What will be the nature of this field
    accountTypeName = models.CharField(max_length=50)
    descriptions = models.TextField(max_length=255, blank=True, null=True)
    createdBy = models.CharField(max_length=25)
    dateCreated = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=25, blank=True, null=True)
    dateModified = models.DateField(auto_now=True)
    approvedBy = models.CharField(max_length=25, blank=True, null=True)
    approvedDate = models.DateField(blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.accountTypeName


class Kyc(models.Model):
    pass


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    accountNo = models.CharField(max_length=25)
    accountName = models.CharField(max_length=100)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    accountType = models.CharField(max_length=50)
    accountTypeId = models.ForeignKey(AccountType, on_delete=models.CASCADE)
    kycId = models.ForeignKey(Kyc, on_delete=models.CASCADE)
    kycStatus = models.BooleanField()
    createdBy = models.CharField(max_length=25)
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
    accountNo = models.CharField(max_length=25)
    accountName = models.CharField(max_length=100)
    activityType = models.CharField(max_length=50)
    userId = models.CharField(max_length=25)  # This should be a foreign key to the user
    dateCreated = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.accountNo} - {self.activityType}"
