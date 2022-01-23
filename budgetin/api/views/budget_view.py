from venv import create
from rest_framework import viewsets
from api.models.budget_model import Budget
from api.serializers.budget_serializer import BudgetSerializer

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.date_format import timestamp_to_dateformat
class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    
    def list(self, request, *args, **kwargs):
        budget = super().list(request, *args, **kwargs)
        for each in budget.data:
            each['created_at'] = timestamp_to_dateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_dateformat(each['updated_at'], "%d %B %Y")
        return budget
    
    def retrieve(self, request, *args, **kwargs):
        budget = super().retrieve(request, *args, **kwargs)
        budget.data['created_at'] = timestamp_to_dateformat(budget.data['created_at'], "%d %B %Y")
        budget.data['updated_at'] = timestamp_to_dateformat(budget.data['updated_at'], "%d %B %Y")
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