
import random
from django.db import models
from django.apps import apps

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def format_timestamp(self, format):
        self.created_at = self.created_at.strftime(format)
        self.updated_at = self.updated_at.strftime(format)

    class Meta:
        abstract = True


class UserTrackModel(models.Model):
    created_by = models.ForeignKey('User', on_delete=models.CASCADE, blank=True, related_name="%(class)s_fk_created", null=True)
    updated_by = models.ForeignKey('User', on_delete=models.CASCADE , null=True, blank=True, related_name="%(class)s_fk_updated")
    class Meta:
        abstract = True
