from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel


class Product(SoftDeleteModel, TimestampModel, UserTrackModel):
    product_code = models.CharField(max_length=200, unique=True)
    product_name = models.CharField(max_length=200)
    strategy = models.ForeignKey('Strategy',on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)