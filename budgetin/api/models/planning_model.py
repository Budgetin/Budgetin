from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import BaseModel

class Strategy(SoftDeleteModel, BaseModel):
    Year = models.IntegerField()
    IsActive = models.BooleanField()
    DueDate = models.DateTimeField()
    LastModifiedBy = models.CharField(max_length=200)