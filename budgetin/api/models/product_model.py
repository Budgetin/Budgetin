from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel


class Product(SoftDeleteModel, TimestampModel, UserTrackModel):
    product_code = models.CharField(max_length=200)
    product_name = models.CharField(max_length=200)
    strategy = models.ForeignKey('Strategy',on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)

    all_object = models.Manager()
    
    def equal(self, product):
       return (
           self.product_name_equal(product.product_name) and
           self.strategy_equal(product.strategy)
       ) 
       
    def product_name_equal(self, product_name):
        try:
            return self.product_name.lower() == product_name.lower()
        except:
            return self.product_name == product_name
    
    def strategy_equal(self, strategy):
        return self.strategy == strategy