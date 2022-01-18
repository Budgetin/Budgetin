from django.db import models


class TimestampModel():
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserTrackModel(models.Model):
    created_by = models.BigIntegerField(blank=True)
    updated_by = models.BigIntegerField(blank=True)

    class Meta:
        abstract = True
