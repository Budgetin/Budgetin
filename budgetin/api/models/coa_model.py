from datetime import datetime
from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel
from api.models.user_model import User

class Coa(SoftDeleteModel, TimestampModel, UserTrackModel):
    name = models.CharField(max_length=200)
    definition = models.CharField(max_length=1000, blank=True, null=True)
    hyperion_name = models.CharField(max_length=200, blank=True, null=True)
    is_capex = models.BooleanField(default=False, blank=True)
    minimum_item_origin = models.BigIntegerField(blank=True, null=True)
    
    def equal(self, coa):
        return (
            self.definition_equal(coa.definition) and 
            self.hyperion_name_equal(coa.hyperion_name) and 
            self.is_capex_equal(coa.is_capex) and
            self.minimum_item_origin_equal(coa.minimum_item_origin)
        )
    
    def definition_equal(self, definition):
        try:
            return self.definition.lower() == definition.lower()
        except:
            return self.definition == definition
    
    def hyperion_name_equal(self, hyperion_name):
        try:
            return self.hyperion_name.lower() == hyperion_name.lower()
        except:
            return self.hyperion_name == hyperion_name

    def is_capex_equal(self, is_capex):
        return self.is_capex == is_capex
    
    def minimum_item_origin_equal(self, minimum_item_origin):
        return self.minimum_item_origin == minimum_item_origin