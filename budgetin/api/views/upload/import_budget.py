from django.utils import timezone

from rest_framework.response import Response

from django.utils.translation import ugettext_lazy as _
from api.models import Budget, Project, ProjectDetail, Planning, Biro, Product, Coa, ProjectType, User
from api.serializers import BudgetSerializer, ProjectSerializer, ProjectDetailSerializer, PlanningSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_file
from api.utils.excel import read_excel, is_empty, export_errors_as_excel

class ImportBudget():
    def start(self, request):
        file = read_file(request)
        df = read_excel(file, 'budget')
        
        '''
            Retrieve data from DB and convert it to Key, Value dictionary.
            This is done to reduce DB calls and optimize searching for specified key with O(1) complexity when searching 
            e.g for product: {'ba001': product (obj), 'ba002': product(obj)}
        '''
        products = dict((product.product_code.lower(), product) for product in Product.objects.all())
        coas = dict((coa.name.lower(), coa) for coa in Coa.objects.all())
        biros = dict((biro.code.lower(), biro) for biro in Biro.objects.all())
        plannings = dict((planning.year, planning) for planning in Planning.objects.all())
        projects = dict((project.project_name.lower(), project) for project in Project.objects.all())
        project_types = dict((project_type.name.lower(), project_type) for project_type in ProjectType.objects.all())
        user = User.objects.get(pk=request.custom_user['id'])
        
        '''
            Key, Value pair for project_details and budgets are more complex.
            e.g for project_detail = {('Rumah Biru', 2021): project_detail (obj), ('Rumah Biru', 2022): project_detail (obj}
        '''
        project_details = dict(((project_detail.project.project_name.lower(), project_detail.planning.year), project_detail) for project_detail in ProjectDetail.objects.select_related('project', 'planning').all())
        budgets = dict(((budget.project_detail.project.project_name.lower(), budget.project_detail.planning.year, budget.coa.name.lower()), budget) for budget in Budget.objects.select_related('project_detail__project', 'project_detail__planning', 'coa').all())
        
        errors = []
        for index, data in df.iterrows():
            print(index)
            errors = self.validate_is_budget(data, index+2, errors)
            errors = self.validate_is_tech(data, index+2, errors)
            errors = self.validate_project(data, index+2, errors)
            product, errors = self.get_product(data, index+2, errors, products)
            coa, errors = self.get_coa(data, index+2, errors, coas)
            biro, errors = self.get_biro(data, index+2, errors, biros)
            
            if not errors:
                planning, plannings = self.get_or_create_planning(request, data, plannings)
                project, projects = self.create_or_update_project(request, data, user, projects, biro, product)
                project_detail, project_details = self.create_or_update_project_detail(request, data, user, project_details, project_types, project, planning)
                self.create_or_update_budget(request, data, user, budgets, project_detail, coa)
            
        if errors:
            return export_errors_as_excel(errors)

        return Response(status=204)
    
    def validate_is_tech(self, data, index, errors):
        is_tech = data['is_tech']
        if is_empty(is_tech):
            errors.append("Row {} - is_tech must be filled".format(index))
        elif is_tech.strip().lower() != 'yes' and is_tech.strip().lower() != 'no':
            errors.append("Row {} - is_tech must be filled with yes/no only".format(index))
        return errors
    
    def validate_is_budget(self, data, index, errors):
        is_budget = data['is_budget']
        if is_empty(is_budget):
            errors.append("Row {} - is_budget must be filled".format(index))
        elif is_budget.strip().lower() != 'yes' and is_budget.strip().lower() != 'no':
            errors.append("Row {} - is_budget must be filled with yes/no only".format(index))
        return errors       
    
    def validate_project(self, data, index, errors):
        name = data['project_name']
        project_type = data['project_type']
        
        if is_empty(name):
            errors.append("Row {} - Project name must be filled".format(index))
        if is_empty(project_type):
            errors.append("Row {} - Project type must be filled".format(index))
            
        return errors
    
    def get_product(self, data, index, errors, products):
        code = data['product_code']
        if is_empty(code):
            errors.append("Row {} - Product code must be filled".format(index))
        else:
            code = code.strip().lower()
            if code in products:
                return products[code], errors
            else:
                errors.append("Row {} - Product code '{}' doesn't exists".format(index, data['product_code']))
        return _, errors
    
    def get_coa(self, data, index, errors, coas):
        name = data['coa_name']
        if is_empty(name):
            errors.append("Row {} - Coa must be filled".format(index))
        else:
            name = name.strip().lower()
            
            is_budget = True if not is_empty(data['is_budget']) and data['is_budget'].lower() == 'yes' else False
            if is_budget and name == 'none':
                errors.append("Row {} - Coa cannot be none if is_budget is 'yes'")
                return _, errors
            
            if name in coas:
                return coas[name], errors
            else:
                errors.append("Row {} - Coa '{}' doesn't exists".format(index, data['coa_name']))
        return _, errors
    
    def get_biro(self, data, index, errors, biros):
        code = data['biro']
        if is_empty(code):
            errors.append("Row {} - Biro must be filled".format(index))
        else:
            code = code.strip().lower()
            
            if code in biros:
                return biros[code], errors
            else:            
                errors.append("Row {} - Biro '{}' doesn't exists".format(index, data['biro']))
        return _, errors
    
    def get_or_create_planning(self, request, data, plannings):
        year = data['year']
        if year in plannings:
            planning = plannings[year]
        else:
            planning = Planning.objects.create(
                year=year,
                is_active = False, #DEBT
                notification = False,
                due_date = timezone.now(),
                created_by_id = request.custom_user['id'],
                updated_by_id = request.custom_user['id'],
            )
            AuditLog.Save(PlanningSerializer(planning), request, ActionEnum.CREATE, TableEnum.PLANNING)
            plannings[year] = planning

        return planning, plannings
    
    def create_or_update_project(self, request, data, user, projects, biro, product):     
        update_dict = {
            'project_description': data['project_description'] if not is_empty(data['project_description']) else None,
            'start_year': data['start_year'] if not is_empty(data['start_year']) else None,
            'end_year': data['end_year'] if not is_empty(data['end_year']) else None,
            'product': product,
            'biro': biro,
            'is_tech': True if not is_empty(data['is_tech']) and data['is_tech'] == 'yes' else False,
            'total_investment_value': data['total_investment_value'] if not is_empty(data['total_investment_value']) else 0,
            'updated_by': user
        }
            
        project_name = data['project_name'].strip()
        new_project = Project(
            project_name = project_name,
            **update_dict
        )
        
        if project_name.lower() not in projects:
            project = self.create_new_project(request, new_project, data['year'])
        else:
            project = projects[project_name.lower()]
            if not project.equal(new_project):
                project = self.update_project(request, project, update_dict)
            
        projects[project_name.lower()] = project
        return project, projects

    def create_new_project(self, request, new_project, year):
        new_project.created_by = new_project.updated_by
        new_project.save()
        new_project.generate_itfamid(year)
        AuditLog.Save(ProjectSerializer(new_project), request, ActionEnum.CREATE, TableEnum.PROJECT)
        return new_project
        
    def update_project(self, request, project, update_dict):
        project = self.update_fields(project, update_dict)
        project.save()
        AuditLog.Save(ProjectSerializer(project), request, ActionEnum.UPDATE, TableEnum.PROJECT)
        return project
    
    def create_or_update_project_detail(self, request, data, user, project_details, project_types, project, planning):
        project_name = project.project_name.lower()
        year = planning.year
        project_type = project_types[data['project_type'].strip().lower()]
        update_dict = {
            'dcsp_id': data['project_id'] if not is_empty(data['project_id']) else None,
            'updated_by': user
        }
            
        new_project_detail = ProjectDetail(
            planning = planning,
            project = project,
            project_type = project_type,
            **update_dict
        )
        
        if (project_name, year) not in project_details:
            project_detail = self.create_new_project_detail(request, new_project_detail)
        else:
            project_detail = project_details[(project_name, year)]
            if not project_detail.equal(new_project_detail):
                self.update_project_detail(request, project_detail, update_dict)
                
        project_details[(project_name, year)] = project_detail
        return project_detail, project_details
    
    def create_new_project_detail(self, request, new_project_detail):
        new_project_detail.created_by = new_project_detail.updated_by
        new_project_detail.save()
        AuditLog.Save(ProjectDetailSerializer(new_project_detail), request, ActionEnum.CREATE, TableEnum.PROJECT_DETAIL)
        return new_project_detail
    
    def update_project_detail(self, request, project_detail, update_dict):
        project_detail = self.update_fields(project_detail, update_dict)
        project_detail.save()
        AuditLog.Save(ProjectDetailSerializer(project_detail), request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)
        return project_detail
    
    def create_or_update_budget(self, request, data, user, budgets, project_detail, coa):
        is_budget = True if not is_empty(data['is_budget']) and data['is_budget'] == 'yes' else False
        project_name = project_detail.project.project_name.lower()
        year = project_detail.planning.year
        coa_name = coa.name.lower()
        
        if not is_budget:
            budget = self.create_empty_budget(request, project_detail)
        else:
            update_dict = {
                'expense_type': data['capex_opex'],
                'planning_q1': data["Q1"] * data["total_budget"],
                'planning_q2': data["Q2"] * data["total_budget"],
                'planning_q3': data["Q3"] * data["total_budget"],
                'planning_q4': data["Q4"] * data["total_budget"],
                'updated_by': user
            }
            
            new_budget = Budget(
                project_detail=project_detail,
                coa=coa,
                **update_dict
            )
            
            if (project_name, year, coa_name) not in budgets:
                budget = self.create_new_budget(request, new_budget)
            else:
                budget = budgets[(project_name, year, coa_name)]
                if not budget.equal(new_budget):
                    self.update_budget(request, budget, update_dict)
                    
        budgets[(project_name, year, coa_name)] = budget
        return budget, budgets
    
    def create_empty_budget(self, request, project_detail):
        coa, _ = Coa.objects.get_or_create(name='None')
        budget = Budget.objects.create(
            project_detail=project_detail,
            coa=coa,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id']
        ) 
        return budget
    
    def create_new_budget(self, request, new_budget):
        new_budget.created_by = new_budget.updated_by
        new_budget.save()
        AuditLog.Save(BudgetSerializer(new_budget), request, ActionEnum.CREATE, TableEnum.BUDGET)
    
    def update_budget(self, request, budget, update_dict):
        budget = self.update_fields(budget, update_dict)
        budget.save()
        AuditLog.Save(BudgetSerializer(budget), request, ActionEnum.UPDATE, TableEnum.BUDGET)
    
    def update_fields(self, model, update_dict):
        for key, value in update_dict.items():
            setattr(model, key, value)
        return model