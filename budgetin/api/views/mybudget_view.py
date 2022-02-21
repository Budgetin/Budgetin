from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from rest_framework.decorators import action

from api.models import Budget
from api.permissions import IsAuthenticated, IsUser
from api.serializers import BudgetResponseSerializer
from api.utils.export_budget import export_budget_as_excel

class MyBudgetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsUser]
     
    def list(self, request):
        user_ithc_biro = request.custom_user['ithc_biro']

        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by').all()
        budgets = budgets.filter(project_detail__project__biro__ithc_biro=user_ithc_biro)
        
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")
            
            
        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        user_ithc_biro = request.custom_user['ithc_biro']
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by'
                                                ).filter(is_active=True)
        budgets = budgets.filter(project_detail__project__biro__ithc_biro=user_ithc_biro)
        
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")

        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def inactive(self, request):
        user_ithc_biro = request.custom_user['ithc_biro']
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by'
                                                ).filter(is_active=False)
        budgets = budgets.filter(project_detail__project__biro__ithc_biro=user_ithc_biro)
        
        for budget in budgets:
            budget.format_timestamp("%d %B %Y")

        serializer = BudgetResponseSerializer(budgets, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='download')
    def export(self, request):
        user_ithc_biro = request.custom_user['ithc_biro']

        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by').all()
        budgets = budgets.filter(project_detail__project__biro__ithc_biro=user_ithc_biro)
        
        return export_budget_as_excel(budgets)