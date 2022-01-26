from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel, UserTrackModel


class Planning(SoftDeleteModel, TimestampModel, UserTrackModel):
    year = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    notification = models.BooleanField(default=False)
    due_date = models.DateTimeField()

    all_object = models.Manager()