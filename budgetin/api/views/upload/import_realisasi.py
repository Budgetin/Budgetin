import pandas
import math

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.exceptions import SheetNotFoundException

from api.models import Coa, ProjectDetail, Budget

def update_db(data):
    dcsp_id = data.pop('BID').split('-')[0]
    coa = get_coa(data.pop('COA'))
    project_detail = get_project_detail(dcsp_id)
    budget_object = get_budget(project_detail, coa)
    # UPDATE THE DATA #
    budget_object.update(
        allocate = is_nan(data['Allocate']),
        returns = is_nan(data['Return']),
        top_up = is_nan(data['Top Up']),
        switching_in = is_nan(data['Switching In']),
        switching_out = is_nan(data['Switching Out']),
        realization_jan = is_nan(data['Jan']),
        realization_feb = is_nan(data['Feb']),
        realization_mar = is_nan(data['Mar']),
        realization_apr = is_nan(data['Apr']),
        realization_may = is_nan(data['May']),
        realization_jun = is_nan(data['Jun']),
        realization_jul = is_nan(data['Jul']),
        realization_aug = is_nan(data['Aug']),
        realization_sep = is_nan(data['Sep']),
        realization_oct = is_nan(data['Oct']),
        realization_nov = is_nan(data['Nov']),
        realization_dec = is_nan(data['Dec']),
    )

def get_coa(coa_name):
    return Coa.objects.get(name=coa_name)

def get_project_detail(dcsp_id):
    return ProjectDetail.objects.filter(dcsp_id = dcsp_id).get()

def get_budget(project_detail, coa):
    return Budget.objects.filter(project_detail=project_detail).filter(coa=coa)

def is_nan(data):
    return 0 if math.isnan(data) else data

class ImportRealisasi(APIView):
    parser_classes = (MultiPartParser, )
    
    @transaction.atomic
    def post(self, request, format=None):
        file_obj = request.FILES['file'].read()
        try:
            df = pandas.read_excel(file_obj, sheet_name='Realisasi')
        except ValueError:
            raise SheetNotFoundException('Realisasi')
        
        
        for index, row in df.iterrows():
            update_db(row)
            
        return Response(status=204)