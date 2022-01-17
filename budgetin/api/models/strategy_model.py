from django.db import models
from api.models.abstract_model import BaseModel

class Strategy(BaseModel):
    name = models.CharField(max_length=200)