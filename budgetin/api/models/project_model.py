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
    total_investment_value = models.BigIntegerField(blank=True, default=0)
    product = models.ForeignKey('Product',on_delete=models.CASCADE)
    is_tech = models.BooleanField(default=False)

    def generate_itfamid(self, year):
        self.itfam_id = str(year) + str(self.id).zfill(7)
        self.save()
        
    def add_total_investment(self, nominal):
        self.total_investment_value += nominal
        self.save()
        
    @staticmethod
    def name_exists(name):
        return Project.objects.filter(project_name__iexact=name).count() > 0
    
    def equal(self, project):
        return (
            self.project_name_equal(project.project_name) and
            self.project_description_equal(project.project_description) and
            self.biro_equal(project.biro) and
            self.start_year_equal(project.start_year) and
            self.end_year_equal(project.end_year) and
            self.total_investment_value_equal(project.total_investment_value) and 
            self.product_equal(project.product) and
            self.is_tech_equal(project.is_tech)
        )
    
    def project_name_equal(self, project_name):
        return self.project_name.lower() == project_name.lower()
    
    def project_description_equal(self, description):
        try:
            return self.project_description.lower() == description.lower()
        except:
            return self.project_description == description
    
    def biro_equal(self, biro):
        return self.biro == biro
    
    def start_year_equal(self, start_year):
        return self.start_year == start_year
    
    def end_year_equal(self, end_year):
        return self.end_year == end_year
    
    def total_investment_value_equal(self, total_investment_value):
        return self.total_investment_value == total_investment_value
    
    def product_equal(self, product):
        return self.product == product
    
    def is_tech_equal(self, is_tech):
        return self.is_tech == is_tech