from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel
from .abstract_model import UserTrackModel

class Budget(SoftDeleteModel, TimestampModel, UserTrackModel):
    ProjectDetailId = models.ForeignKey('ProjectDetail', on_delete=models.CASCADE)
    CoaId = models.ForeignKey('Coa', on_delete=models.CASCADE)
    ExpenseType = models.CharField(max_length=200)
    PlanningNomimal = models.CharField(max_length=200)
    PlanningQ1 = models.BigIntegerField()
    PlanningQ2 = models.BigIntegerField()
    PlanningQ3 = models.BigIntegerField()
    PlanningQ4 = models.BigIntegerField()
    RealizationNominal = models.BigIntegerField()
    RealizationJan = models.BigIntegerField()
    RealizationFeb = models.BigIntegerField()
    RealizationMar = models.BigIntegerField()
    RealizationApr = models.BigIntegerField()
    RealizationMay = models.BigIntegerField()
    RealizationJun = models.BigIntegerField()
    RealizationJul = models.BigIntegerField()
    RealizationAug = models.BigIntegerField()
    RealizationSep = models.BigIntegerField()
    RealizationOct = models.BigIntegerField()
    RealizationNov = models.BigIntegerField()
    RealizationDec = models.BigIntegerField()
    SwitchingIn = models.BigIntegerField()
    SwitchingOut = models.BigIntegerField()
    TopUp = models.BigIntegerField()
    Return = models.BigIntegerField()
    Allocate = models.BigIntegerField()