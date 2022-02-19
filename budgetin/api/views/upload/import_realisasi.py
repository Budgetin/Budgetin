from django.forms import model_to_dict
import pandas
import math

from django.db import transaction
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.exceptions import SheetNotFoundException, NotFoundException, ImportValidationException
from api.utils.enum import ActionEnum, TableEnum, SwitchingTypeEnum
from api.utils.auditlog import AuditLog
from api.serializers import RealizationSerializer, SwitchingSerializer, ProjectDetailResponseSerializer
from api.models import Realization, Switching
from django.db.models.base import ObjectDoesNotExist

from api.models import Coa, ProjectDetail, Budget, Planning

def update_db(request, index, data):
    dcsp_id = data.pop('BID').split('-')[0]
    coa = get_coa(index, data.pop('COA'))
    planning = get_planning(index, data.pop('Tahun'))
    project_detail = get_project_detail(index, dcsp_id, planning)
    budget_object = get_budget(index, project_detail, coa).get()

    #INSERT TO REALIZATION
    try:
        realization, created = Realization.objects.update_or_create(
            budget=budget_object, 
            coa=coa,
            defaults={
                'coa': coa,
                'budget': budget_object,
                'realization_jan' : is_nan(data['Jan']),
                'realization_feb' : is_nan(data['Feb']),
                'realization_mar' : is_nan(data['Mar']),
                'realization_apr' : is_nan(data['Apr']),
                'realization_may' : is_nan(data['May']),
                'realization_jun' : is_nan(data['Jun']),
                'realization_jul' : is_nan(data['Jul']),
                'realization_aug' : is_nan(data['Aug']),
                'realization_sep' : is_nan(data['Sep']),
                'realization_oct' : is_nan(data['Oct']),
                'realization_nov' : is_nan(data['Nov']),
                'realization_dec' : is_nan(data['Dec']),
                'allocate' : is_nan(data['Allocate']),
                'updated_by_id' : request.custom_user['id']
            }
        )
        if created:
            update = Realization.objects.filter(budget=budget_object).filter(coa=coa).update(created_by_id=request.custom_user['id'])
            if update:
                AuditLog.Save(RealizationSerializer(realization), request, ActionEnum.CREATE, TableEnum.REALIZATION)
        else:
            AuditLog.Save(RealizationSerializer(realization), request, ActionEnum.UPDATE, TableEnum.REALIZATION)
        
    #SWITCHING
        switching_in = is_nan(data['Switching In'])
        switching_out = is_nan(data['Switching Out'])
        returns = is_nan(data['Return'])
        topup = is_nan(data['Top Up'])
        
        if switching_in:
            nominal = switching_in
            to_plus = budget_object

            #Get all data in switching
            sw_in_data = Switching.objects.filter(to_plus=to_plus).filter(Q(type=SwitchingTypeEnum.SWITCH.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_IN.value)).all()
            total = 0
            for sw in sw_in_data:
                total += sw.nominal
            
            '''
                If total is greater than nominal
                    The switch type is correction and the final_nominal should be negative
                else
                    final_nominal is positive
            '''

            if total > nominal:
                final_nominal = nominal - total
                type = SwitchingTypeEnum.CORRECTION_SWITCHING_IN.value
            else:
                final_nominal = nominal - total
                type = SwitchingTypeEnum.SWITCH.value
            
            '''If final_nominal is 0 (no changes on the nominal, dont create a new switching)'''
            if final_nominal:
                switching = Switching.objects.create(
                    nominal = final_nominal,
                    to_plus = to_plus,
                    type = type
                )
                #DEBT ADD TO AUDITLOG
                
        if switching_out:
            nominal = switching_out
            from_minus = budget_object
            #Get all data in switching
            sw_in_data = Switching.objects.filter(from_minus=from_minus).filter(Q(type=SwitchingTypeEnum.SWITCH.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_OUT.value)).all()
            total = 0
            for sw in sw_in_data:
                total += sw.nominal
            if total > nominal:
                final_nominal = nominal - total
                type = SwitchingTypeEnum.CORRECTION_SWITCHING_OUT.value
            else:
                final_nominal = nominal - total
                type = SwitchingTypeEnum.SWITCH.value

            if final_nominal:
                switching = Switching.objects.create(
                    nominal = final_nominal,
                    from_minus = from_minus,
                    type = type
                )

        if returns:
            nominal = returns
            from_minus = budget_object
            #Get all data in switching
            sw_in_data = Switching.objects.filter(from_minus=from_minus).filter(Q(type=SwitchingTypeEnum.RETURN.value) | Q(type=SwitchingTypeEnum.CORRECTION_RETURN.value)).all()
            total = 0
            for sw in sw_in_data:
                total += sw.nominal
            
            
            if total > nominal:
                final_nominal = nominal - total
                type = SwitchingTypeEnum.CORRECTION_RETURN.value
            else:
                final_nominal = nominal - total
                type = SwitchingTypeEnum.RETURN.value

            if final_nominal:
                switching = Switching.objects.create(
                    nominal = final_nominal,
                    from_minus = from_minus,
                    type = type
                )

        if topup:
            nominal = topup
            to_plus = budget_object
            #Get all data in switching
            sw_in_data = Switching.objects.filter(to_plus=to_plus).filter(Q(type=SwitchingTypeEnum.TOPUP.value)|Q(type=SwitchingTypeEnum.CORRETCTION_TOPUP.value)).all()
            total = 0
            for sw in sw_in_data:
                total += sw.nominal

            print("total = " + str(total))
            print("nominal = "+ str(nominal))
            if total > nominal:
                final_nominal = nominal - total
                type = SwitchingTypeEnum.CORRETCTION_TOPUP.value
            else:
                final_nominal = nominal-total
                type = SwitchingTypeEnum.TOPUP.value

            if final_nominal:
                switching = Switching.objects.create(
                    nominal = final_nominal,
                    to_plus = to_plus,
                    type = type
                )

    except TypeError:
        raise ImportValidationException("Wrong input type on line " + str(index))

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