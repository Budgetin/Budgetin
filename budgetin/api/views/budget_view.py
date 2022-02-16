from django.forms import model_to_dict
from django.db import transaction

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Budget, Project, ProjectDetail, Monitoring
from api.serializers import BudgetSerializer, BudgetResponseSerializer, ProjectSerializer, ProjectDetailSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.permissions import IsAuthenticated
from api.utils.export_budget import export_as_excel

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

            AuditLog.Save(ProjectSerializer(project), request, ActionEnum.CREATE, TableEnum.PROJECT)
            project.generate_itfamid()
        else:
            project = Project.objects.get(pk=request.data['project_id'])

        # Project Detail
        project_detail, created = ProjectDetail.objects.update_or_create(planning_id=request.data['planning'], project=project, defaults={
            'project_type_id': request.data['project_type']
        })
        print("wololo   "+str(created))
        if created:
            ProjectDetail.objects.filter(planning_id=request.data['planning']).filter(project=project).update( 
                created_by_id = request.custom_user['id'],
                updated_by_id = request.custom_user['id']
            )
            AuditLog.Save(ProjectDetailSerializer(project_detail), request, ActionEnum.CREATE, TableEnum.PROJECT_DETAIL)
        else:
            ProjectDetail.objects.filter(planning_id=request.data['planning']).filter(project=project).update(
                updated_by_id = request.custom_user['id'])
            AuditLog.Save(ProjectDetailSerializer(project_detail), request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)
           
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
                AuditLog.Save(BudgetSerializer(updated_budget), request, ActionEnum.CREATE, TableEnum.BUDGET)
            else:
                Budget.objects.filter(project_detail=project_detail).filter(coa_id = budget['coa']).update(updated_by_id = request.custom_user['id'])
                
                AuditLog.Save(BudgetSerializer(updated_budget), request, ActionEnum.UPDATE, TableEnum.BUDGET)
            print(model_to_dict(updated_budget))
        
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

    @action(methods=['post'], detail=True)
    def restore(self, request, pk=None):
        request.data['updated_by'] = request.custom_user['id']
        request.data['is_active'] = True
        budget = super().update(request, [], {'pk':pk})
        AuditLog.Save(budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        
        return Response({"message" : "Budget re-activated"})
    
    @action(methods=['get'], detail=False)
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
    
    @action(methods=['get'], detail=False)
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

    @action(methods=['get'], detail=False, url_path='download')
    def export(self, request):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by').all()

        return export_as_excel(budgets)