from tracemalloc import start
import pandas
import math

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from datetime import datetime

from api.models import Biro, Coa, Product, Strategy, Project, Planning, ProjectDetail, ProjectType, Budget
from api.utils.hit_api import get_all_biro
from api.utils.enum import ProjectTypeEnum
from api.exceptions import PlanningSheetNotFoundException, ImportValidationException


'''
Validasi
 - Harus ada sheet 'Planning'
 - Format Kolom Product -> Product Code - Product Name. 
   - Product Name ga boleh kosong
   - Product code yang sama harus memiliki name yang sama
   - Product code yang sama harus memiliki strategy yang sama
 - Project name yang sama harus memiliki product yang sama
 - Project name yang sama harus memiliki biro yang sama
 - Project name yang sama harus memiliki is_tech yang sama
 - Budget planning pada tahun yang sama harus memiliki Project Type yang sama
'''

###

def create_update_all_biro():
    biros = get_all_biro('manager_employee,sub_group,sub_group.group,manager_employee,sub_group.manager_employee,sub_group.group.manager_employee')
    for biro in biros:
        create_update_biro(biro)

def create_update_biro(biro):
    return Biro.objects.update_or_create(
        ithc_biro=biro['id'],
        defaults={'code': biro['code'], 
                    'name': biro['name'],
                    'sub_group_code': biro['sub_group']['code'],
                    'group_code': biro['sub_group']['group']['code'],
                    'rcc': biro['sub_group']['rcc'],
                    }
        )
    
def insert_to_db(request, data):
    biro = Biro.objects.filter(code=data['Biro']).first()
    coa, _ = get_or_create_coa(request, data['COA'])
    strategy, _ = get_or_create_strategy(request, data['Strategy'])
    product, _ = get_or_create_product(request, data['Product'], strategy)
    project, _ = get_or_create_project(request, data, biro, product)
    planning, _ = get_or_create_planning(request, data['Tahun'])
    project_detail, _ = get_or_create_project_detail(request, data, project, planning)
    create_budget(request, data, project_detail, coa)
    

def get_or_create_coa(request, coa_name):
    return Coa.objects.get_or_create(name=coa_name, defaults={
        'is_capex': True, #DEBT
        'minimum_item_origin': 500000000, #DEBT
        'created_by_id': request.custom_user['id'],
        'updated_by_id': request.custom_user['id'],
    })
    
def get_or_create_strategy(request, strategy_name):
    return Strategy.objects.get_or_create(name=strategy_name, defaults={
        'created_by_id': request.custom_user['id'],
        'updated_by_id': request.custom_user['id'],
    })
    
def get_or_create_product(request, product, strategy):
    product_code, product_name = get_product_code_and_name(product)
    validate_product(product_code, product_name, strategy)
    
    return Product.objects.get_or_create(product_code=product_code, defaults={
        'product_name': product_name,
        'strategy': strategy,
        'created_by_id': request.custom_user['id'],
        'updated_by_id': request.custom_user['id'],
    })    
    
def get_product_code_and_name(product):
    splits = product.split('-')
    if len(splits) <= 1:
        raise ImportValidationException('Invalid Product Column. Expected: Product Code - Product Name. Found: ' + product)
    product_code = splits[0]
    splits.pop(0)
    product_name = '-'.join(splits)
    
    return product_code, product_name

def validate_product(product_code, product_name, strategy):
    product = Product.objects.filter(product_code=product_code).first()
    if product:
        if product.strategy != strategy:
            message = 'Inconsistent Product Strategy. Product Code - ' + product_code + '. Existing Strategy - ' + product.strategy.name + '. Found Strategy - ' + strategy.name
            raise ImportValidationException(message)
        if product.product_name != product_name:
            message = 'Inconsistent Product Name. Product Code - ' + product_code + '. Existing Product Name - ' + product.product_name + '. Found Product Name - ' + product_name
            raise ImportValidationException(message)
        
def get_or_create_project(request, data, biro, product):
    project_name = data['Project Name']
    project_description = data['Project Description']
    start_year = data['Tahun'] if math.isnan(data['Tahun Mulai']) else data['Tahun Mulai']
    end_year = data['Tahun'] if math.isnan(data['Tahun Selesai']) else data['Tahun Selesai']
    total_investment_value = data['Total Investment']
    product = product
    is_tech = True if data['Tech/Non Tech'] == 'Tech' else False
    
    validate_project(project_name, product, biro, is_tech)
    
    project, created = Project.objects.get_or_create(project_name=project_name, defaults={
        'project_description': project_description,
        'start_year': start_year,
        'end_year': end_year,
        'total_investment_value': total_investment_value,
        'biro': biro,
        'product': product,
        'is_tech': is_tech,
        'created_by_id': request.custom_user['id'],
        'updated_by_id': request.custom_user['id'],
    })
    project.generate_itfamid()
    
    return project, created

def validate_project(project_name, product, biro, is_tech):
    project = Project.objects.filter(project_name=project_name).first()
    if project:
        if project.product != product:
            message = 'Inconsistent Project Product (' + project_name + '). Existing Product: ' + project.product.product_code + '. Found Product: ' + product.product_code
            raise ImportValidationException(message)
        if project.biro != biro:
            message = 'Inconsistent Project Biro (' + project_name + '). Existing Biro: ' + project.biro.code + '. Found Biro: ' + biro.code
            raise ImportValidationException(message)
        if project.is_tech != is_tech:
            message = 'Inconsistent Project Tech/Non Tech (' + project_name + '). Existing project is type of ' + get_is_tech_str(project.is_tech) + '. Found project is type of ' + get_is_tech_str(is_tech)
            raise ImportValidationException(message)
        
def get_is_tech_str(is_tech):
    return "Tech" if is_tech else "Non Tech"

def get_or_create_planning(request, year):
    return Planning.objects.get_or_create(year=year, defaults={
        'is_active': False, #DEBT
        'notification': False,
        'due_date': datetime.now(),
        'created_by_id': request.custom_user['id'],
        'updated_by_id': request.custom_user['id'],
    })
    
def get_or_create_project_detail(request, data, project, planning):
    project_type = get_project_type(data['Project Type'])
    validate_project_detail(project, planning, project_type)
    
    return ProjectDetail.objects.get_or_create(project=project, planning=planning, defaults={
        'dcsp_id': data['Project ID'],
        'project_type': get_project_type(data['Project Type']),
        'created_by_id': request.custom_user['id'],
        'updated_by_id': request.custom_user['id'],
    })

def validate_project_detail(project, planning, project_type):
    project_detail = ProjectDetail.objects.filter(project=project, planning=planning).first()
    if project_detail:
        if project_detail.project_type != project_type:
            message = 'Inconsistent Project Type (' + project.project_name + '). Existing Project Type: ' + project_detail.project_type.name + '. Found Project Type: ' + project_type.name
            raise ImportValidationException(message)

def get_project_type(type):
    project_type, _ = ProjectType.objects.get_or_create(name=type)
    return project_type

def create_budget(request, data, project_detail, coa):
    budget = Budget(
        project_detail = project_detail,
        coa = coa,
        expense_type = data["CAPEX/OPEX"],
        planning_q1 = data["Q1"] * data["Total Budget"],
        planning_q2 = data["Q2"] * data["Total Budget"],
        planning_q3 = data["Q3"] * data["Total Budget"],
        planning_q4 = data["Q4"] * data["Total Budget"],
        created_by_id = request.custom_user['id'],
        updated_by_id = request.custom_user['id'],
    )
    budget.save()

class ImportListPlanning(APIView):
    parser_classes = (MultiPartParser, )
    
    @transaction.atomic
    def post(self, request, format=None):
        file_obj = request.FILES['file'].read()
        try:
            df = pandas.read_excel(file_obj, sheet_name='Planning')
        except ValueError:
            raise PlanningSheetNotFoundException()
        
        create_update_all_biro()
        
        for index, row in df.iterrows():
            insert_to_db(request, row)
            
        return Response(status=204)