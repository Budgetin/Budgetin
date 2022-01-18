from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel, UserTrackModel


class PicBudget(SoftDeleteModel, TimestampModel, UserTrackModel):
    biro_id = models.BigIntegerField()
    employee_id = models.BigIntegerField()
