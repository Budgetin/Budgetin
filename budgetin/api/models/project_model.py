from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel, UserTrackModel



class Project(SoftDeleteModel, TimestampModel, UserTrackModel):
    itfam_id = models.CharField(max_length=200)
    project_name = models.CharField(max_length=200)
    project_description = models.CharField(max_length=500)
    biro_id = models.BigIntegerField()
    rcc = models.IntegerField()
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    total_investment_value = models.BigIntegerField()
    # product_id = models.ForeignKey('Product',on_delete=models.CASCADE)
    is_tech = models.BooleanField(default=False)
