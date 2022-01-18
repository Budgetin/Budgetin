from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel, UserTrackModel


class Planning(SoftDeleteModel, TimestampModel, UserTrackModel):
    Year = models.IntegerField()
    IsActive = models.BooleanField(default=True)
    DueDate = models.DateTimeField()
