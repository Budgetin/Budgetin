from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel

class Project(SoftDeleteModel, TimestampModel, UserTrackModel):
    itfam_id = models.CharField(max_length=200, blank=True)
    project_name = models.CharField(max_length=200)
    project_description = models.CharField(max_length=500, blank=True, null=True)
    biro = models.ForeignKey('Biro', on_delete=models.CASCADE)
    start_year = models.IntegerField(blank=True, null=True)
    end_year = models.IntegerField(blank=True, null=True)
    total_investment_value = models.BigIntegerField()
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    is_tech = models.BooleanField(default=False)

    def generate_itfamid(self):
        self.itfam_id = str(self.start_year) + str(self.id).zfill(8)
        self.save()