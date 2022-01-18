from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel


class Monitoring(SoftDeleteModel, TimestampModel):
    biro_id = models.BigIntegerField()
    monitoring_status_id = models.ForeignKey('MonitoringStatus',on_delete=models.CASCADE)