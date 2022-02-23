from django.db import models
from django_softdelete.models import SoftDeleteModel
from api.models.abstract_model import TimestampModel, UserTrackModel

class Realization(SoftDeleteModel, TimestampModel, UserTrackModel):
    #DEBT add parent either ProjectDetail or Budget
    project_detail = models.ForeignKey('ProjectDetail', on_delete=models.CASCADE, blank=True, null=True)
    coa = models.ForeignKey('Coa', on_delete=models.CASCADE)
    budget = models.ForeignKey('Budget', on_delete=models.CASCADE, blank=True, null=True)
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
    allocate = models.BigIntegerField(default = 0, blank = True)