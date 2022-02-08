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
        request.data['updated_by'] = request.custom_user['id']
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
        request.data['is_active'] = False
        budget = super().update(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        
        return Response({"message" : "Budget deactivated"})

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        request.data['updated_by'] = request.custom_user['id']
        request.data['is_active'] = True
        budget = super().update(request, [], {'pk':pk})
        AuditLog.Save(budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        
        return Response({"message" : "Budget re-activated"})
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by'
                                                ).filter(is_active=True)
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")

        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactive(self, request):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by'
                                                ).filter(is_active=False)
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")

        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)

    def list_for_export():
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy').all()
        
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")
            
        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)