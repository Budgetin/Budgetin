from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel

class Biro(SoftDeleteModel, TimestampModel):
    ithc_biro = models.BigIntegerField()
    rcc = models.IntegerField(blank=True, null=True)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=200)
    sub_group_code = models.CharField(max_length=10)
    group_code = models.CharField(max_length=10)

    all_object = models.Manager()
    
    @staticmethod
    def code_exists(code):
        return Biro.objects.filter(code__iexact=code).count() > 0