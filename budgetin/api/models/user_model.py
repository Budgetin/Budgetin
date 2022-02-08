from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel

class User(TimestampModel, UserTrackModel, SoftDeleteModel):
    employee_id = models.BigIntegerField(unique=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, unique=True)
    initial = models.CharField(max_length=10, blank=True, null=True)
    eselon = models.CharField(max_length=10, blank=True, null=True)
    role = models.CharField(max_length=100, default='user')
    is_active = models.BooleanField(default=True)
