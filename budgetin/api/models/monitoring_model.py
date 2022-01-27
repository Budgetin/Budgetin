from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel


class Monitoring(SoftDeleteModel, TimestampModel):
    biro = models.ForeignKey('Biro', on_delete=models.CASCADE)
    monitoring_status = models.ForeignKey('MonitoringStatus',on_delete=models.CASCADE)
    planning = models.ForeignKey('Planning', on_delete=models.CASCADE)
    pic_employee_id = models.BigIntegerField()
    pic_initial = models.CharField(max_length=10, blank=True)
    pic_display_name = models.CharField(max_length=50, blank=True)