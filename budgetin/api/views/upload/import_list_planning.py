from tracemalloc import start
import pandas

from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from datetime import datetime

from api.models import Biro, Coa, Product, Strategy, Project, Planning, ProjectDetail
from api.utils.hit_api import get_all_biro

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
    
def insert_to_db(data):
    biro = Biro.objects.filter(code=data['Biro']).first()
    # coa, _ = get_or_create_coa(data['COA'])
    product, _ = get_or_create_product(data['PRODUCT ID']) #DEBT, nama kolom nya begimana? ditembak static begini
    project, _ = get_or_create_project(data, biro, product)
    planning, _ = get_or_create_planning(data['TAHUN'])
    project_detail, _ = get_or_create_project_detail(data, project, planning)
    

def get_or_create_coa(coa_name):
    return Coa.objects.get_or_create(name=coa_name, defaults={
        'created_by': 1, #DEBT
        'is_capex': True, #DEBT
        'minimum_item_origin': 500000000 #DEBT
    })
    
def get_or_create_product(product):
    product_code, product_name = get_product_code_and_name(product)
    strategy = Strategy.objects.all().first()
    
    return Product.objects.get_or_create(product_code=product_code, defaults={
        'created_by': 1, #DEBT
        'product_name': product_name,
        'strategy': strategy #DEBT
    })
    
def get_product_code_and_name(product):
    splits = product.split('-')
    product_code = splits[0]
    splits.pop(0)
    product_name = '-'.join(splits)
    
    return product_code, product_name
    
def get_or_create_project(data, biro, product):
    itfam_id = '20210102' #DEBT
    project_name = data['Project Masked'] #DEBT
    project_description = data['Project Masked'] #DEBT
    start_year = data['TAHUN']
    end_year = data['TAHUN SELESAI']
    total_investment_value = data['TOTAL BUDGET']
    product = product
    # is_tech = models.BooleanField(default=False)
    
    return Project.objects.get_or_create(itfam_id=itfam_id, defaults={
        'project_name': project_name,
        'project_description': project_description,
        'start_year': start_year,
        'end_year': end_year,
        'total_investment_value': total_investment_value,
        'biro': biro,
        'product': product,
    })

def get_or_create_planning(year):
    return Planning.objects.get_or_create(year=year, defaults={
        'is_active': False, #DEBT
        'notification': False,
        'due_date': datetime.now(),
    })
    
def get_or_create_project_detail(data, project, planning):
    return ProjectDetail.objects.get_or_create() #DEBT

class ImportListPlanning(APIView):
    parser_classes = (MultiPartParser, )
    
    def post(self, request, format=None):
        file_obj = request.FILES['file'].read()
        df = pandas.read_excel(file_obj)
        
        # create_update_all_biro()
        
        for index, row in df.iterrows():
            insert_to_db(row)
        
        return Response(status=204)