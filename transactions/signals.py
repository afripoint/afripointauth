from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction, TransactionLog


@receiver(post_save, sender=Transaction)
def create_transaction_log(sender, instance, created, **kwargs):
    if created:
        TransactionLog.objects.create(
            transaction_id=instance.transaction_id,
            user_id=instance.user_id,
            transaction_type=instance.transaction_type,
            amount=instance.amount,
            payment_method=instance.payment_method,
            transaction_status=instance.transaction_status,
            timestamp=instance.timestamp,
            error_message=instance.error_message,
            additional_details=instance.additional_details,
        )
