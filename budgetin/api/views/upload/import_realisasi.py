from django.forms import model_to_dict
import pandas
import math

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.exceptions import SheetNotFoundException, NotFoundException, ImportValidationException
from api.utils.enum import ActionEnum, TableEnum
from api.utils.auditlog import AuditLog
from django.db.models.base import ObjectDoesNotExist

from api.models import Coa, ProjectDetail, Budget, Planning

def update_db(request, index, data):
    dcsp_id = data.pop('BID').split('-')[0]
    coa = get_coa(index, data.pop('COA'))
    planning = get_planning(index, data.pop('Tahun'))
    project_detail = get_project_detail(index, dcsp_id, planning)
    budget_object = get_budget(index, project_detail, coa)
    try:
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
    except TypeError:
        raise ImportValidationException("Wrong input type on line " + str(index))
    AuditLog.Save(budget_object.get(), request, ActionEnum.UPDATE, TableEnum.BUDGET)

def get_coa(index, coa_name):
    try:
        return Coa.objects.get(name=coa_name)
    except ObjectDoesNotExist:
        raise NotFoundException("COA with name "+str(coa_name)+" on line "+str(index))
    
def get_project_detail(index, dcsp_id, planning):
    try:
        return ProjectDetail.objects.filter(planning = planning).filter(dcsp_id = dcsp_id).get()
    except ObjectDoesNotExist:
        raise NotFoundException("Project Detail with dcsp_id "+dcsp_id +" and year "+ str(model_to_dict(planning)['year'])+" on line "+str(index))

def get_planning(index, year):
    try:
        return Planning.objects.filter(year = year).get()
    except ObjectDoesNotExist:
        raise NotFoundException("Planning with year "+ str(year)+" on line "+str(index))

def get_budget(index, project_detail, coa):
    try:
        return Budget.objects.filter(project_detail=project_detail).filter(coa=coa)
    except ObjectDoesNotExist:
        raise NotFoundException("Budget"+" on line "+str(index))

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
            update_db(request, (index+2), row)
            
        return Response(status=204)