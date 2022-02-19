from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel


class Product(SoftDeleteModel, TimestampModel, UserTrackModel):
    product_code = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    strategy = models.ForeignKey('Strategy',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    all_object = models.Manager()
    
    @staticmethod
    def code_exists(code):
        return Product.objects.filter(product_code__iexact=code).count() > 0
    
    @staticmethod
    def name_exists(name):
        return Product.objects.filter(product_name__iexact=name).count() > 0