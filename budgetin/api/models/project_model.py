from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel, UserTrackModel



class Project(SoftDeleteModel, TimestampModel, UserTrackModel):
    ITFamId = models.CharField(max_length=200)
    ProjectName = models.CharField(max_length=200)
    ProjectDescription = models.CharField(max_length=500)
    BiroId = models.BigIntegerField()
    RCC = models.IntegerField()
    StartYear = models.IntegerField()
    EndYear = models.IntegerField()
    TotalInvestmentValue = models.BigIntegerField()
    # ProductId = models.ForeignKey('Product',on_delete=models.CASCADE)
    isTech = models.BooleanField(default=False)
