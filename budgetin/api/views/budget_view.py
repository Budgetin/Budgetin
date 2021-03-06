import pandas as pd
from io import BytesIO
from django.utils import timezone
from django.forms import model_to_dict
from django.db import transaction
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Budget, Project, ProjectDetail, Monitoring, Planning, Biro, Product, Coa
from api.serializers import BudgetSerializer, BudgetResponseSerializer, ProjectSerializer, ProjectDetailSerializer, MonitoringBaseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum, RoleEnum, MonitoringStatusEnum
from api.permissions import IsAuthenticated
from api.views.upload.import_budget import ImportBudget
from api.utils.export_budget import export_budget_as_excel
from api.utils.file import get_import_template_path
from api.utils.excel import export_excel, write_sheet
from api.exceptions import ValidationException

def active_planning(planning_id):
    planning = Planning.objects.get(pk=planning_id)
    return planning.is_active

def user_eligible(request):
    # Admin, eligible to create budget in all biro
    role = request.custom_user['role']
    if role.lower() == RoleEnum.ADMIN.value.lower():
        return True

    # User, only eligible to create budget in his/her biro only for planning that is not yet submitted
    biro_id = request.data['biro']
    biro = Biro.objects.get(pk=biro_id)
    user_ithc_biro = request.custom_user['ithc_biro']
    if user_ithc_biro == biro.ithc_biro:
        planning_id = request.data['planning']
        monitoring = Monitoring.objects.select_related('planning').get(biro=biro, planning=planning_id)
        if monitoring.monitoring_status.lower() == MonitoringStatusEnum.SUBMITTED.value.lower():
            raise ValidationException('Your budget planning for ' + str(monitoring.planning.year) + ' is already submitted. Please contact admin for further assistance')
        
        return True
    
    return False

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
        planning_id = request.data['planning']
        
        if not active_planning(planning_id):
            raise ValidationException('Selected planning is currently inactive.')
        
        if not user_eligible(request):
            raise ValidationException('You are not eligible to add budget to this biro')
        
        project = self.create_or_update_project(request)
        project_detail = self.create_or_update_project_detail(request, project)
        self.create_budget(request, project_detail)
        
        #Tag Monitoring of this Biro to Draft
        Monitoring.objects.filter(planning_id=request.data['planning']).update(monitoring_status="Draft")
        
        return Response(model_to_dict(project))

    def create_or_update_project(self, request):
        planning = Planning.objects.get(pk=request.data['planning'])
        if 'project_id' not in request.data:
            project_name = request.data['project_name']
            if Project.name_exists(project_name):
                raise ValidationException('Project {} already exists.'.format(project_name))
            
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
            project.generate_itfamid(planning.year)
            AuditLog.Save(ProjectSerializer(project), request, ActionEnum.CREATE, TableEnum.PROJECT)
        else:            
            project = Project.objects.get(pk=request.data['project_id'])
            project.project_description = request.data['project_description']
            project.start_year = request.data['start_year']
            project.end_year = request.data['end_year']
            project.total_investment_value = request.data['total_investment_value']
            project.product_id = request.data['product']
            project.is_tech = request.data['is_tech']
            project.updated_by_id = request.custom_user['id']
            project.save()
            
            AuditLog.Save(ProjectSerializer(project), request, ActionEnum.UPDATE, TableEnum.PROJECT)
        
        project.refresh_from_db()
        return project

    def create_or_update_project_detail(self, request, project):
        project_detail, created = ProjectDetail.objects.update_or_create(planning_id=request.data['planning'], project=project, defaults={
            'project_type_id': request.data['project_type']
        })
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
        
        project_detail.refresh_from_db()
        return project_detail
    
    def create_budget(self, request, project_detail):
        if len(request.data['budget']) == 0:
            if not self.is_budget_exists(project_detail):
                budget = self.create_empty_budget(request, project_detail)
                AuditLog.Save(BudgetSerializer(budget), request, ActionEnum.CREATE, TableEnum.BUDGET)
        else:
            for budget in request.data['budget']:
                coa, _ = Coa.objects.get_or_create(name="None")
                updated_budget, budget_created = Budget.objects.update_or_create(project_detail=project_detail, coa=coa, defaults={
                    'coa_id': budget['coa'],
                    'expense_type': budget['expense_type'],
                    'planning_q1': budget['planning_q1'],
                    'planning_q2': budget['planning_q2'],
                    'planning_q3':budget['planning_q3'],
                    'planning_q4': budget['planning_q4']
                })
                if budget_created:
                    Budget.objects.filter(project_detail=project_detail).filter(coa_id = budget['coa']).update(
                        created_by_id = request.custom_user['id'],
                        updated_by_id = request.custom_user['id']
                    )
                    AuditLog.Save(BudgetSerializer(updated_budget), request, ActionEnum.CREATE, TableEnum.BUDGET)
                else:
                    Budget.objects.filter(project_detail=project_detail).filter(coa_id = budget['coa']).update(updated_by_id = request.custom_user['id'])
                    
                    AuditLog.Save(BudgetSerializer(updated_budget), request, ActionEnum.UPDATE, TableEnum.BUDGET)
    
    def is_budget_exists(self, project_detail):
        return Budget.objects.filter(project_detail=project_detail).count() > 0
        
    def create_empty_budget(self, request, project_detail):
        coa, _ = Coa.objects.get_or_create(name='None')
        budget = Budget.objects.create(
            project_detail=project_detail,
            coa=coa,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id']
        ) 
        return budget
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        budget = super().update(request, *args, **kwargs)
        AuditLog.Save(budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        return budget

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        deleted_budget = Budget.objects.get(pk=kwargs['pk'])
        budget = super().destroy(request, *args, **kwargs)
        
        remaining_budget = Budget.objects.filter(project_detail_id=deleted_budget.project_detail_id).count()
        deleted_pd = ProjectDetail.objects.select_related('project').get(pk=deleted_budget.project_detail_id)
        planning_id = deleted_pd.planning_id
        biro = deleted_pd.project.biro_id
        if not remaining_budget:
            ProjectDetail.objects.filter(pk = deleted_budget.project_detail_id).update(
                is_deleted = True,
                deleted_at = timezone.now()
            )
            #Special for auditlog project detail
            rewritten_req = request
            rewritten_req.parser_context['kwargs']['pk'] = deleted_budget.project_detail_id
            AuditLog.Save(ProjectDetailSerializer(deleted_pd), rewritten_req, ActionEnum.DELETE, TableEnum.PROJECT_DETAIL)

        #check if there is any project detail left for monitoring x
        remaining_pd = ProjectDetail.objects.select_related('project', 'project__biro').filter(planning_id = planning_id).filter(project__biro_id=biro).count()
        if not remaining_pd:
            updated_monitoring = Monitoring.objects.filter(planning_id=planning_id).filter(biro_id=biro).get()
            Monitoring.objects.filter(planning_id=planning_id).filter(biro_id=biro).update(
                monitoring_status = 'To Do'
            )
            AuditLog.Save(MonitoringBaseSerializer(updated_monitoring), request, ActionEnum.UPDATE, TableEnum.MONITORING)
        #ENDSEQ
        AuditLog.Save(budget, request, ActionEnum.DELETE, TableEnum.BUDGET)
        return budget
    
    @transaction.atomic
    @action(methods=['post'], detail=True)
    def deactivate(self, request, pk=None):
        Budget.objects.filter(pk=pk).update(
            updated_by = request.custom_user['id'],
            is_active = False
        )
        updated_budget = Budget.objects.get(pk=pk)
        AuditLog.Save(BudgetSerializer(updated_budget), request, ActionEnum.UPDATE, TableEnum.BUDGET)
        
        return Response({"message" : "Budget deactivated"})

    @transaction.atomic
    @action(methods=['post'], detail=True)
    def restore(self, request, pk=None):
        request.data['updated_by'] = request.custom_user['id']
        request.data['is_active'] = True
        budget = super().update(request, [], {'pk':pk})
        AuditLog.Save(budget, request, ActionEnum.UPDATE, TableEnum.BUDGET)
        
        return Response({"message" : "Budget re-activated"})

    @transaction.atomic
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

    @transaction.atomic
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

    @action(methods=['get'], detail=False, url_path='export')
    def export(self, request):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by').all()

        return export_budget_as_excel(budgets)
    
    @action(methods=['post'], detail=False, url_path='import')
    @transaction.atomic
    def import_from_excel(self, request):
        return ImportBudget().start(request)
        
    @action(methods=['get'], detail=False, url_path='import/template')
    def download_import_template(self, request):
        file_path = get_import_template_path(TableEnum.BUDGET)
        book = load_workbook(filename=file_path)

        self.write_product_sheet(book, file_path)
        self.write_coa_sheet(book, file_path)

        book.close()                
        file_content = BytesIO(save_virtual_workbook(book))
        return export_excel(content=file_content, filename='import_template_product.xlsx')
    
    def write_product_sheet(self, book, file_path):
        dataframe = self.get_product_dataframe()
        write_sheet(
            book=book,
            file_path=file_path,
            dataframe=dataframe,
            sheet_name='existing_product'
        )
    
    def get_product_dataframe(self):
        columns = ['product_code', 'product_name', 'strategy']
        products = Product.objects.select_related('strategy').all()
        result = []
        for product in products:
            temp = []
            strategy = product.strategy
            
            temp.append(product.product_code)
            temp.append(product.product_name)
            temp.append(strategy.name if strategy else '')
            result.append(temp)
        return pd.DataFrame(result, columns=columns)
    
    def write_coa_sheet(self, book, file_path):
        dataframe = self.get_coa_dataframe()
        write_sheet(
            book=book,
            file_path=file_path,
            dataframe=dataframe,
            sheet_name='existing_coa'
        )
    
    def get_coa_dataframe(self):
        columns = ['coa_name', 'hyperion_name', 'coa_definition']
        coas = Coa.objects.all()
        result = []
        for coa in coas:
            temp = []
            temp.append(coa.name)
            temp.append(coa.hyperion_name)
            temp.append(coa.definition)
            result.append(temp)
            
        return pd.DataFrame(result, columns=columns)
    