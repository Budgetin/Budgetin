from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel

class Budget(SoftDeleteModel, TimestampModel, UserTrackModel):
    #related_name buat backward join (dari table ProjectDetail)
    project_detail = models.ForeignKey('ProjectDetail', on_delete=models.CASCADE, related_name='budget', blank=True)
    coa = models.ForeignKey('Coa', on_delete=models.CASCADE, null=True)
    expense_type = models.CharField(max_length=200, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    planning_q1 = models.BigIntegerField(default = 0, blank = True)
    planning_q2 = models.BigIntegerField(default = 0, blank = True)
    planning_q3 = models.BigIntegerField(default = 0, blank = True)
    planning_q4 = models.BigIntegerField(default = 0, blank = True)
    allocate = models.BigIntegerField(default = 0, blank = True)
    is_active = models.BooleanField(default=True, blank = True)