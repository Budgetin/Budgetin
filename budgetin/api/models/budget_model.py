from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel
from .abstract_model import UserTrackModel

class Budget(SoftDeleteModel, TimestampModel, UserTrackModel):
    ProjectDetailId = models.ForeignKey('ProjectDetail', on_delete=models.CASCADE)
    CoaId = models.ForeignKey('Coa', on_delete=models.CASCADE)
    ExpenseType = models.CharField(max_length=200)
    PlanningNomimal = models.CharField(max_length=200)
    PlanningQ1 = models.IntegerField()
    PlanningQ2 = models.IntegerField()
    PlanningQ3 = models.IntegerField()
    PlanningQ4 = models.IntegerField()
    RealizationNominal = models.IntegerField()
    RealizationJan = models.IntegerField()
    RealizationFeb = models.IntegerField()
    RealizationMar = models.IntegerField()
    RealizationApr = models.IntegerField()
    RealizationMay = models.IntegerField()
    RealizationJun = models.IntegerField()
    RealizationJul = models.IntegerField()
    RealizationAug = models.IntegerField()
    RealizationSep = models.IntegerField()
    RealizationOct = models.IntegerField()
    RealizationNov = models.IntegerField()
    RealizationDec = models.IntegerField()
    SwitchingIn = models.IntegerField()
    SwitchingOut = models.IntegerField()
    TopUp = models.IntegerField()
    Return = models.IntegerField()
    Allocate = models.IntegerField()