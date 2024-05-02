from django.db import models
import uuid


class TimeStampedModel(models.Model):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    createdBy = models.CharField(max_length=25, blank=True, null=True)
    dateCreated = models.DateField(auto_now_add=True)
    modifiedBy = models.CharField(max_length=25, blank=True, null=True)
    dateModified = models.DateField(auto_now=True)
    approvedBy = models.CharField(max_length=25, blank=True, null=True)
    approvedDate = models.DateField(blank=True, null=True)

    class Meta:
        abstract = True
