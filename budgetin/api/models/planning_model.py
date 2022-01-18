from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel, UserTrackModel


class Planning(SoftDeleteModel, TimestampModel, UserTrackModel):
    year = models.IntegerField()
    is_active = models.BooleanField(default=True)
    due_date = models.DateTimeField()
