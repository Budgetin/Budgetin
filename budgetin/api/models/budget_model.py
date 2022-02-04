from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel

class Budget(SoftDeleteModel, TimestampModel, UserTrackModel):
    #related_name buat backward join (dari table ProjectDetail)
    project_detail = models.ForeignKey('ProjectDetail', on_delete=models.CASCADE, related_name='budget')
    coa = models.ForeignKey('Coa', on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=200)
    planning_q1 = models.BigIntegerField(default = 0, blank = True)
    planning_q2 = models.BigIntegerField(default = 0, blank = True)
    planning_q3 = models.BigIntegerField(default = 0, blank = True)
    planning_q4 = models.BigIntegerField(default = 0, blank = True)
    realization_jan = models.BigIntegerField(default = 0, blank = True)
    realization_feb = models.BigIntegerField(default = 0, blank = True)
    realization_mar = models.BigIntegerField(default = 0, blank = True)
    realization_apr = models.BigIntegerField(default = 0, blank = True)
    realization_may = models.BigIntegerField(default = 0, blank = True)
    realization_jun = models.BigIntegerField(default = 0, blank = True)
    realization_jul = models.BigIntegerField(default = 0, blank = True)
    realization_aug = models.BigIntegerField(default = 0, blank = True)
    realization_sep = models.BigIntegerField(default = 0, blank = True)
    realization_oct = models.BigIntegerField(default = 0, blank = True)
    realization_nov = models.BigIntegerField(default = 0, blank = True)
    realization_dec = models.BigIntegerField(default = 0, blank = True)
    switching_in = models.BigIntegerField(default = 0, blank = True)
    switching_out = models.BigIntegerField(default = 0, blank = True)
    top_up = models.BigIntegerField(default = 0, blank = True)
    returns = models.BigIntegerField(default = 0, blank = True)
    allocate = models.BigIntegerField(default = 0, blank = True)