from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel

class Budget(SoftDeleteModel, TimestampModel, UserTrackModel):
    #related_name buat backward join (dari table ProjectDetail)
    project_detail = models.ForeignKey('ProjectDetail', on_delete=models.CASCADE, related_name='budget', blank=True)
    coa = models.ForeignKey('Coa', on_delete=models.CASCADE, null=True)
    expense_type = models.CharField(max_length=200, blank=True, null=True)
    notes = models.CharField(max_length=500, blank=True, null=True)
    planning_q1 = models.BigIntegerField(default = 0, blank = True)
    planning_q2 = models.BigIntegerField(default = 0, blank = True)
    planning_q3 = models.BigIntegerField(default = 0, blank = True)
    planning_q4 = models.BigIntegerField(default = 0, blank = True)
    allocate = models.BigIntegerField(default = 0, blank = True)
    is_active = models.BooleanField(default=True, blank = True)
    
    def equal(self, budget):
        return (
            self.expense_type_equal(budget.expense_type) and
            self.planning_q1_equal(budget.planning_q1) and
            self.planning_q2_equal(budget.planning_q2) and
            self.planning_q3_equal(budget.planning_q3) and
            self.planning_q4_equal(budget.planning_q4)
        )
    
    def expense_type_equal(self, expense_type):
        return self.expense_type.lower() == expense_type.lower()
    
    def planning_q1_equal(self, planning_q1):
        return round(self.planning_q1) == round(planning_q1)
    
    def planning_q2_equal(self, planning_q2):
        return round(self.planning_q2) == round(planning_q2)
    
    def planning_q3_equal(self, planning_q3):
        return round(self.planning_q3) == round(planning_q3)
    
    def planning_q4_equal(self, planning_q4):
        return round(self.planning_q4) == round(planning_q4)
    