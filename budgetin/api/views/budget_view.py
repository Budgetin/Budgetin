from django.forms import model_to_dict
from django.db import transaction

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Budget, Project, ProjectDetail, Monitoring
from api.serializers import BudgetSerializer, BudgetResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.permissions import IsAuthenticated, IsAdmin

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        # Project
        if 'project_id' not in request.data:
            project = Project.objects.create(
                project_name = request.data['project_name'],
                project_description = request.data['project_description'],
                biro_id = request.data['biro'],
                start_year = request.data['start_year'],
                end_year = request.data['end_year'],
                total_investment_value = request.data['total_investment_value'],
                product_id = request.data['product'],
                is_tech = request.data['is_tech'],
                created_by_id = request.custom_user['id'],
                updated_by_id = request.custom_user['id']
            )

            AuditLog.Save(project, request, ActionEnum.CREATE, TableEnum.PROJECT)
            project.generate_itfamid()
        else:
            project = Project.objects.get(pk=request.data['project_id'])
            
        
        # Project Detail
        project_detail, created = ProjectDetail.objects.update_or_create(planning_id=request.data['planning'], project=project, defaults={
            'project_type_id': request.data['project_type']
        })
        
        if created:
            ProjectDetail.objects.filter(planning_id=request.data['planning']).filter(project=project).update( 
                created_by_id = request.custom_user['id'],
                updated_by_id = request.custom_user['id']
            )
            AuditLog.Save(project_detail, request, ActionEnum.CREATE, TableEnum.PROJECT_DETAIL)
        else:
            ProjectDetail.objects.filter(planning_id=request.data['planning']).filter(project=project).update(
                updated_by_id = request.custom_user['id'])
            AuditLog.Save(project_detail, request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)
           
        # Budget
        if len(request.data['budget']) == 0:
            budget = Budget.objects.create(project_detail=project_detail, coa=None)
            AuditLog.Save(budget, request, ActionEnum.CREATE, TableEnum.BUDGET)
        for budget in request.data['budget']:
            updated_budget, budget_created = Budget.objects.update_or_create(project_detail=project_detail, coa=None, defaults={
                'coa_id': budget['coa'],
                'expense_type': budget['expense_type'],
                'planning_q1': budget['planning_q1'],
                'planning_q2': budget['planning_q2'],
                'planning_q3':budget['planning_q3'],
                'planning_q4': budget['planning_q4']
            })
            if budget_created:
                # print(Budget.objects.filter(project_detail=project_detail).filter(coa_id = budget['coa']).get())
                Budget.objects.filter(project_detail=project_detail).filter(coa_id = budget['coa']).update(
                created_by_id = request.custom_user['id'],
                updated_by_id = request.custom_user['id']
                )
                AuditLog.Save(updated_budget, request, ActionEnum.CREATE, TableEnum.BUDGET)
            else:
                Budget.objects.filter(project_detail=project_detail).filter(coa_id = budget['coa']).update(updated_by_id = request.custom_user['id'])
                
                AuditLog.Save(updated_budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        
        #Tag Monitoring of this Biro to Draft
        monitoring = Monitoring.objects.filter(planning_id=request.data['planning']).update(monitoring_status="Draft")
            
        return Response(model_to_dict(project))

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