from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel


class Monitoring(SoftDeleteModel, TimestampModel, UserTrackModel):
    biro = models.ForeignKey('Biro', on_delete=models.CASCADE, blank=True)
    monitoring_status = models.CharField(max_length=50)
    planning = models.ForeignKey('Planning', on_delete=models.CASCADE, blank=True)
    pic_employee_id = models.BigIntegerField(blank=True)
    pic_initial = models.CharField(max_length=10, blank=True)
    pic_display_name = models.CharField(max_length=50, blank=True)