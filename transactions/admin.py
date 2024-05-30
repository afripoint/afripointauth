from django.contrib import admin
from .models import Transaction, TransactionDetails, TransactionLog

admin.site.register(Transaction)
admin.site.register(TransactionDetails)


class TransactionLogAdmin(admin.ModelAdmin):
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

    def get_readonly_fields(self, request, obj=None):
        return ["transaction_id"]


admin.site.register(TransactionLog, TransactionLogAdmin)
