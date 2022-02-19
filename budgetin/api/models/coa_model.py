from datetime import datetime
from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel
from api.models.user_model import User

class Coa(SoftDeleteModel, TimestampModel, UserTrackModel):
    name = models.CharField(max_length=200)
    definition = models.CharField(max_length=1000, blank=True, null=True)
    hyperion_name = models.CharField(max_length=200, blank=True, null=True)
    is_capex = models.BooleanField(default=False, blank=True)
    minimum_item_origin = models.BigIntegerField(blank=True, null=True)
    
    @staticmethod
    def name_exists(name):
        return Coa.objects.filter(name__iexact=name).count() > 0