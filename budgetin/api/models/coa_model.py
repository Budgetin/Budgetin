from datetime import datetime
from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel
from api.models.user_model import User

class Coa(SoftDeleteModel, TimestampModel, UserTrackModel):
    name = models.CharField(max_length=200)
    definition = models.CharField(max_length=1000, blank=True, null=True)
    hyperion_name = models.CharField(max_length=200)
    is_capex = models.BooleanField(default=False)
    minimum_item_origin = models.BigIntegerField(blank=True, null=True)

    def format_timestamp(self):
        self.created_at = self.created_at.strftime("%d %B %Y")
        self.updated_at = self.updated_at.strftime("%d %B %Y")
        
    def format_created_updated_by(self):
        self.created_by = User.objects.get(pk=self.created_by).display_name
        if self.updated_by:
            self.updated_by = User.objects.get(pk=self.updated_by).display_name
        else:
            self.updated_by = ''