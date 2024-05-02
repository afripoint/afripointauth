import logging
from django.utils.timezone import now


class AccountActivityLogHandler(logging.Handler):
    def emit(self, record):
        from customaccounts.models import (
            AccountActivity,
        )

        try:
            log_entry = AccountActivity(
                activityType=record.levelname,
                userId=record.getMessage(),  # Customize this based on actual log message structure
                accountName="Log Entry",  # Set this appropriately
                accountNo="Log",  # Set this appropriately
            )
            log_entry.save()
        except Exception:
            self.handleError(record)
