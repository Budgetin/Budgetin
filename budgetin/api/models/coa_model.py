from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel


class Coa(SoftDeleteModel, TimestampModel):
    name = models.CharField(max_length=200, unique=True)
    definition = models.CharField(max_length=1000)
    hyperion_name = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_capex = models.BooleanField(default=False)
    minimum_item_origin = models.IntegerField(blank=True, null=True)
