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

from api.models import Budget, Project, ProjectDetail, Monitoring, Planning, Biro, Product, Coa, ProjectType
from api.serializers import BudgetSerializer, BudgetResponseSerializer, ProjectSerializer, ProjectDetailSerializer, MonitoringBaseSerializer, PlanningSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum, RoleEnum, MonitoringStatusEnum
from api.permissions import IsAuthenticated
from api.utils.export_budget import export_budget_as_excel
from api.utils.file import read_excel, read_file, get_import_template_path, remove_sheet, export_excel
from api.utils.hit_api import get_all_biro
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
        planning = Planning.objects.filter(planning__id=request.data['planning'])
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
                budget = Budget.objects.create(
                    project_detail=project_detail,
                    coa=None,
                    created_by_id = request.custom_user['id'],
                    updated_by_id = request.custom_user['id']
                )
                AuditLog.Save(BudgetSerializer(budget), request, ActionEnum.CREATE, TableEnum.BUDGET)
        else:
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
        file = read_file(request)
        df = read_excel(file, 'budget')
        errors = []
        
        self.create_update_all_biro()
        
        for index, data in df.iterrows():
            print(index)
            errors = self.insert_to_db(request, data, (index+2), errors)
            
        if errors:
            raise ValidationException(errors)

        return Response(status=204)
    
    def create_update_all_biro(self):
        biros = get_all_biro('manager_employee,sub_group,sub_group.group,manager_employee,sub_group.manager_employee,sub_group.group.manager_employee')
        for biro in biros:
            self.create_update_biro(biro)

    def create_update_biro(self, biro):
        return Biro.objects.update_or_create(
            ithc_biro=biro['id'],
            defaults={
                'code': biro['code'], 
                'name': biro['name'],
                'sub_group_code': biro['sub_group']['code'],
                'group_code': biro['sub_group']['group']['code'],
                'rcc': biro['sub_group']['rcc'],
            }
        )
    
    def insert_to_db(self, request, data, index, errors):
        errors.extend(self.validate_data(data, index))
        
        if not errors:
            product = Product.objects.filter(product_code__iexact=data['product_code']).first()
            coa = Coa.objects.filter(name__iexact=data['coa_name']).first()
            biro = Biro.objects.filter(code__iexact=data['biro']).first()
            planning = self.get_or_create_planning(request, data['year'])
            project = self.create_or_update_project_from_excel(request, data, biro, product)
            project_detail = self.get_or_create_project_detail(request, data, project, planning)
            self.create_or_update_budget(request, data, project_detail, coa)
            
        return errors
    
    def get_or_create_planning(self, request, year):
        planning, created = Planning.objects.get_or_create(year=year, defaults={
            'is_active': False, #DEBT
            'notification': False,
            'due_date': timezone.now(),
            'created_by_id': request.custom_user['id'],
            'updated_by_id': request.custom_user['id'],
        })

        if created:
            AuditLog.Save(PlanningSerializer(planning), request, ActionEnum.CREATE, TableEnum.PLANNING)

        return planning
    
    def create_or_update_project_from_excel(self, request, data, biro, product):
        project_name = data['project_name']
        project_description = data['project_description'] if not pd.isnull(data['project_description']) else None
        year = data['year']
        start_year = data['start_year'] if not pd.isnull(data['start_year']) else None
        end_year = data['end_year'] if not pd.isnull(data['end_year']) else None
        product = product
        is_tech = True if data['is_tech'] == 'Tech' else False
        
        project, created = Project.objects.update_or_create(project_name__iexact=project_name, defaults={
            'project_name': project_name,
            'project_description': project_description,
            'start_year': start_year,
            'end_year': end_year,
            'biro': biro,
            'product': product,
            'is_tech': is_tech,
            'created_by_id': request.custom_user['id'],
            'updated_by_id': request.custom_user['id'],
        })

        if created:
            project.generate_itfamid(year)
            AuditLog.Save(ProjectSerializer(project), request, ActionEnum.CREATE, TableEnum.PROJECT)
                    
        return project
    
    def get_or_create_project_detail(self, request, data, project, planning):
        project_type = ProjectType.objects.filter(name__iexact=data['project_type']).first()
        
        project_detail, created = ProjectDetail.objects.get_or_create(project=project, planning=planning, defaults={
            'dcsp_id': data['project_id'],
            'project_type': project_type,
            'created_by_id': request.custom_user['id'],
            'updated_by_id': request.custom_user['id'],
        })

        if created:
            AuditLog.Save(ProjectDetailSerializer(project_detail), request, ActionEnum.CREATE, TableEnum.PROJECT_DETAIL)

        return project_detail
    
    def create_or_update_budget(self, request, data, project_detail, coa):
        budget = Budget.objects.select_related(
            'project_detail', 'project_detail__project'
        ).filter(project_detail=project_detail, coa=coa).first()
        
        if budget:
            project = budget.project_detail.project
            project.total_investment_value -= (budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4)
            
            budget.expense_type = data['capex_opex']
            budget.planning_q1 = data["Q1"] * data["total_budget"]
            budget.planning_q2 = data["Q2"] * data["total_budget"]
            budget.planning_q3 = data["Q3"] * data["total_budget"]
            budget.planning_q4 = data["Q4"] * data["total_budget"]
            budget.updated_by_id = request.custom_user['id']
            budget.save()
            
            project.total_investment_value += (budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4)
            project.save()
            AuditLog.Save(BudgetSerializer(budget), request, ActionEnum.UPDATE, TableEnum.BUDGET)
        else:
            project = Project.objects.filter(project_detail=project_detail).first()
            project.add_total_investment(data['total_budget'])
            
            budget = Budget.objects.create(
                project_detail = project_detail,
                coa = coa,
                expense_type = data['capex_opex'],
                planning_q1 = data["Q1"] * data["total_budget"],
                planning_q2 = data["Q2"] * data["total_budget"],
                planning_q3 = data["Q3"] * data["total_budget"],
                planning_q4 = data["Q4"] * data["total_budget"],
                created_by_id = request.custom_user['id'],
                updated_by_id = request.custom_user['id'],
            )
            
            AuditLog.Save(BudgetSerializer(budget), request, ActionEnum.CREATE, TableEnum.BUDGET)
        
    def validate_data(self, data, index):
        errors = []
        errors = self.validate_product(data, index, errors)
        errors = self.validate_coa(data, index, errors)
        errors = self.validate_biro(data, index, errors)
        errors = self.validate_project(data, index, errors)
        return errors
    
    def validate_product(self, data, index, errors):
        code = data['product_code']
        if pd.isnull(code):
            errors.append("Product code must be filled at line {}".format(index))
        elif not Product.code_exists(code):
            errors.append("Product code '{}' at line {} doesn't exists".format(code, index))
        return errors
    
    def validate_coa(self, data, index, errors):
        name = data['coa_name']
        if not Coa.name_exists(name):
            errors.append("Coa '{}' at line {} doesn't exists".format(name, index))
        return errors
    
    def validate_biro(self, data, index, errors):
        code = data['biro']
        if not Biro.code_exists(code):
            errors.append("Biro '{}' at line {} doesn't exists".format(code, index))
        return errors
    
    def validate_project(self, data, index, errors):
        name = data['project_name']
        description = data['project_description'] if not pd.isnull(data['project_description']) else None
        is_tech = True if data['is_tech'] == 'Tech' else False
        project_type = data['project_type']
        biro = data['biro']
        year = data['year']
        
        if pd.isnull(name):
            errors.append("Project name must be filled at line {}".format(index))
        if pd.isnull(is_tech):
            errors.append("Is Tech must be filled at line {}".format(index))
        if pd.isnull(project_type):
            errors.append("Project type must be filled at line {}".format(index))
        
        existing_project = Project.objects.select_related('biro').filter(project_name__iexact=name).first()
        if existing_project:
            if description and description != existing_project.project_description:
                errors.append("Inconsistent project description at line {}. Existing project description is '{}'".format(index, existing_project.project_description))
            if not pd.isnull(is_tech) and is_tech != existing_project.is_tech:
                errors.append("Inconsistent project tech/non tech at line {}. Existing project is a type of '{}'".format(index, 'Tech' if existing_project.is_tech else 'Non Tech'))
            if not pd.isnull(biro) and biro.lower() != existing_project.biro.code.lower():
                errors.append("Inconsistent project biro at line {}. Existing project is owned by '{}'".format(index, existing_project.biro.zcode))
            
            if not pd.isnull(project_type):
                existing_project = Project.objects.prefetch_related(
                    'project_detail', 
                    'project_detail__planning',
                    'project_detail__project_type'
                ).filter(project_name__iexact=name, project_detail__planning__year=year).first()
                
                if existing_project:
                    existing_project_detail = existing_project.project_detail.filter(planning__year=year).first()
                    existing_project_type = existing_project_detail.project_type.name
                    if project_type.lower() != existing_project_type.lower():
                        errors.append("Inconsistent project type at line {}. Existing project type is '{}'".format(index, existing_project_type))
        return errors

    def create_strategy(self, request, data):
        return Budget.objects.create(
            name = data['strategy_name'],
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )
        
    @action(methods=['get'], detail=False, url_path='import/template')
    def download_import_template(self, request):
        file_path = get_import_template_path(TableEnum.BUDGET)
        book = load_workbook(filename=file_path)

        self.write_product_sheet(book, file_path)
        self.write_coa_sheet(book, file_path)

        book.close()                
        return export_excel(content=BytesIO(save_virtual_workbook(book)), filename='import_template_product.xlsx')
    
    def write_product_sheet(self, book, file_path):
        columns = ['product_code', 'product_name', 'strategy']
        products = self.get_all_product()
        
        writer = pd.ExcelWriter(file_path, engine = 'openpyxl')
        writer.book = book
        
        if 'existing_product' in book.sheetnames:
            remove_sheet(book, 'existing_product')            
            
        df = pd.DataFrame(products, columns=columns)
        df.to_excel(writer, sheet_name = 'existing_product', index=False)
        writer.save()
        writer.close()
    
    def get_all_product(self):
        products = Product.objects.select_related('strategy').all()
        result = []
        for product in products:
            temp = []
            strategy = product.strategy
            
            temp.append(product.product_code)
            temp.append(product.product_name)
            temp.append(strategy.name if strategy else '')
            result.append(temp)
        return result
    
    def write_coa_sheet(self, book, file_path):
        columns = ['coa_name', 'hyperion_name', 'coa_definition']
        coas = self.get_all_coa()
        
        writer = pd.ExcelWriter(file_path, engine = 'openpyxl')
        writer.book = book
        
        if 'existing_coa' in book.sheetnames:
            remove_sheet(book, 'existing_coa')            
            
        df = pd.DataFrame(coas, columns=columns)
        df.to_excel(writer, sheet_name = 'existing_coa', index=False)
        writer.save()
        writer.close()
    
    def get_all_coa(self):
        coas = Coa.objects.all()
        result = []
        for coa in coas:
            temp = []
            temp.append(coa.name)
            temp.append(coa.hyperion_name)
            temp.append(coa.definition)
            result.append(temp)
        return result
    