from django.db import models


class LogEntry(models.Model):
    level = models.CharField(max_length=10)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
