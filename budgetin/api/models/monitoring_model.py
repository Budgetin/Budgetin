from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel


class Monitoring(SoftDeleteModel, TimestampModel):
    biro_id = models.BigIntegerField()
    monitoring_status = models.ForeignKey('MonitoringStatus',on_delete=models.CASCADE)
    planning = models.ForeignKey('Planning', on_delete=models.CASCADE)
    pic_employee_id = models.BigIntegerField()
    pic_initial = models.CharField(max_length=10, blank=True)
    pic_display_name = models.CharField(max_length=50, blank=True)