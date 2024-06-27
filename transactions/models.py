from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth import get_user_model

User = get_user_model()


TRANSACTION_TYPE = (
    ("bill_payment", "Bill Payment"),
    ("cable_subscription", "Cable Subscription"),
    ("data_purchase", "Data Purchase"),
    ("electricity", "Electricity"),
    ("airtime_purchase", "Airtime Purchase"),
    ("fund transfer", "Fund Transfer"),
    ("purchase", "Purchase"),
)

PAYMENT_METHOD = (
    ("bank_transfer", "Bank Transfer"),
    ("debit_card", "Debit card"),
    ("ewallet", "E-Wallet"),
)

STATUS = (
    ("success", "Success"),
    ("pending", "Pending"),
    ("failed", "Failed"),
)


class Transaction(models.Model):
    transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50, choices=TRANSACTION_TYPE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHOD)
    transaction_status = models.CharField(max_length=10, choices=STATUS)
    timestamp = models.DateTimeField(default=timezone.now)
    error_message = models.CharField(max_length=255, blank=True, null=True)
    additional_details = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transaction"

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.transaction_type}"


class TransactionDetails(models.Model):
    transaction = models.ForeignKey(
        Transaction, on_delete=models.CASCADE, related_name="details"
    )
    vendor_id = models.CharField(max_length=50)
    account_id = models.CharField(max_length=50)
    invoice_id = models.CharField(max_length=50)
    transaction_description = models.TextField(blank=True, null=True)
    transaction_reference = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Transaction Detail"
        verbose_name_plural = "Transaction Details"

    def __str__(self):
        return f"Details for Transaction {self.transaction.transaction_id}"


class TransactionLog(models.Model):
    transaction_id = models.CharField(max_length=255)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50)
    transaction_status = models.CharField(max_length=50)
    timestamp = models.DateTimeField(default=timezone.now)
    error_message = models.CharField(max_length=255, blank=True, null=True)
    additional_details = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Transaction Log"
        verbose_name_plural = "Transaction Logs"

    def __str__(self):
        return f"Encrypted Transaction {self.transaction_id} - {self.transaction_type}"
