from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel


class Table(SoftDeleteModel, TimestampModel):
    name = models.CharField(max_length=200)
