from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel

class Strategy(SoftDeleteModel, TimestampModel, UserTrackModel):
    name = models.CharField(max_length=200,unique=True)
    
    all_objects = models.Manager()
