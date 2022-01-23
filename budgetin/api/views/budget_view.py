from venv import create
from rest_framework import viewsets
from api.models.budget_model import Budget
from api.serializers.budget_serializer import BudgetSerializer
from datetime import datetime

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    
    def list(self, request, *args, **kwargs):
        budget = super().list(request, *args, **kwargs)
        for each in budget.data:
            createdDate = each['created_at']
            date_time_obj = datetime.fromisoformat(createdDate)
            each['created_at'] = date_time_obj.strftime("%d %B %Y")

            updatedDate = each['updated_at']
            date_time_obj = datetime.fromisoformat(updatedDate)
            each['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return budget
    
    def retrieve(self, request, *args, **kwargs):
        budget = super().retrieve(request, *args, **kwargs)
        createdDate = budget.data['created_at']
        date_time_obj = datetime.fromisoformat(createdDate)
        budget.data['created_at'] = date_time_obj.strftime("%d %B %Y")

        updatedDate = budget.data['updated_at']
        date_time_obj = datetime.fromisoformat(updatedDate)
        budget.data['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return budget

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        budget = super().create(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.CREATE, TableEnum.BUDGET)
        return budget

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        budget = super().update(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        return budget

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        budget = super().destroy(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.DELETE, TableEnum.BUDGET)
        return budget