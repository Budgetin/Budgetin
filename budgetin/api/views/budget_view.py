from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Budget
from api.serializers import BudgetSerializer, BudgetResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.date_format import timestamp_to_strdateformat

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    
    def list(self, request, *args, **kwargs):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by').all()
        
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")
            
        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        budget = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by').get(pk=kwargs['pk'])
        budget.format_timestamp("%d %B %Y")
        
        serializer = BudgetResponseSerializer(budget, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.custom_user['id']
        budget = super().create(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.CREATE, TableEnum.BUDGET)
        return budget

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        budget = super().update(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        return budget

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']                       
        budget = super().destroy(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.DELETE, TableEnum.BUDGET)
        return budget

    def list_for_export():
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy').all()
        
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")
            
        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)