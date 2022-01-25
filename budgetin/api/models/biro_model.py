from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel

class Biro(SoftDeleteModel, TimestampModel):
    ithc_biro = models.BigIntegerField()
    code = models.CharField(max_length=200)
    name = models.CharField(max_length=200)