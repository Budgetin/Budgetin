from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import BaseModel

class Action(SoftDeleteModel, BaseModel):
    name = models.CharField(max_length=200)