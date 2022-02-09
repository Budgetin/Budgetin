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
from api.exceptions import PlanningSheetNotFoundException


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
    product, _ = get_or_create_product(request, data['Product ID'], strategy)
    project, _ = get_or_create_project(request, data, biro, product)
    planning, _ = get_or_create_planning(request, data['Tahun'])
    project_detail, _ = get_or_create_project_detail(request, data, project, planning)
    create_budget(request, data, project_detail, coa)
    

def get_or_create_coa(request, coa_name):
    return Coa.objects.get_or_create(name=coa_name, defaults={
        'created_by': request.custom_user['id'],
        'is_capex': True, #DEBT
        'minimum_item_origin': 500000000 #DEBT
    })
    
def get_or_create_strategy(request, strategy_name):
    return Strategy.objects.get_or_create(name=strategy_name, defaults={
        'created_by': request.custom_user['id'],
    })
    
def get_or_create_product(request, product, strategy):
    product_code, product_name = get_product_code_and_name(product)
    
    return Product.objects.get_or_create(product_code=product_code, defaults={
        'created_by': request.custom_user['id'],
        'product_name': product_name,
        'strategy': strategy
    })    
    
def get_product_code_and_name(product):
    splits = product.split('-')
    product_code = splits[0]
    splits.pop(0)
    product_name = '-'.join(splits)
    
    return product_code, product_name
    
def get_or_create_project(request, data, biro, product):
    project_name = data['Project Name']
    project_description = data['Project Description']
    start_year = data['Tahun'] if math.isnan(data['Tahun Mulai']) else data['Tahun Mulai']
    end_year = data['Tahun'] if math.isnan(data['Tahun Selesai']) else data['Tahun Selesai']
    total_investment_value = data['Total Investment']
    product = product
    is_tech = data['Tech/Non Tech']
    
    project, created = Project.objects.get_or_create(project_name=project_name, defaults={
        'project_description': project_description,
        'start_year': start_year,
        'end_year': end_year,
        'total_investment_value': total_investment_value,
        'biro': biro,
        'product': product,
        'is_tech': True if is_tech == 'Tech' else False,
        'created_by': request.custom_user['id']
    })
    project.generate_itfamid()
    
    return project, created

def get_or_create_planning(request, year):
    return Planning.objects.get_or_create(year=year, defaults={
        'is_active': False, #DEBT
        'notification': False,
        'due_date': datetime.now(),
        'created_by': request.custom_user['id'],
    })
    
def get_or_create_project_detail(request, data, project, planning):
    return ProjectDetail.objects.get_or_create(planning=planning, project=project, defaults={
        'dcsp_id': data['Project ID'],
        'project_type': get_project_type(data['Project Type']),
        'created_by': request.custom_user['id'],
    })

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
        created_by = request.custom_user['id'],
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