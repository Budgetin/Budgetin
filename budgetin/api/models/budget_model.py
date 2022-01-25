from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel
from .abstract_model import UserTrackModel

class Budget(SoftDeleteModel, TimestampModel, UserTrackModel):
    project_detail = models.ForeignKey('ProjectDetail', on_delete=models.CASCADE)
    coa = models.ForeignKey('Coa', on_delete=models.CASCADE)
    expense_type = models.CharField(max_length=200)
    planning_q1 = models.BigIntegerField()
    planning_q2 = models.BigIntegerField()
    planning_q3 = models.BigIntegerField()
    planning_q4 = models.BigIntegerField()
    realization_jan = models.BigIntegerField()
    realization_feb = models.BigIntegerField()
    realization_mar = models.BigIntegerField()
    realization_apr = models.BigIntegerField()
    realization_may = models.BigIntegerField()
    realization_jun = models.BigIntegerField()
    realization_jul = models.BigIntegerField()
    realization_aug = models.BigIntegerField()
    realization_sep = models.BigIntegerField()
    realization_oct = models.BigIntegerField()
    realization_nov = models.BigIntegerField()
    realization_dec = models.BigIntegerField()
    switching_in = models.BigIntegerField()
    switching_out = models.BigIntegerField()
    top_up = models.BigIntegerField()
    returns = models.BigIntegerField()
    allocate = models.BigIntegerField()