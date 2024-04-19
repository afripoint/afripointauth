import logging

# Do not import Django models at the top of the file


class DbLogHandler(logging.Handler):
    def emit(self, record):
        from applogger.models import (
            LogEntry,
        )

        try:
            # Now you can safely use your Django models
            LogEntry.objects.get_or_create(
                level=record.levelname, message=self.format(record)
            )
        except Exception as e:
            # It's a good idea to handle exceptions here to avoid breaking the logging process
            # You might want to log to a file or stdout as a fallback
            print(f"Failed to log to db: {e}")
