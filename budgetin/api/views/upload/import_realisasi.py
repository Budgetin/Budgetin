from django.forms import model_to_dict
import pandas
import math

from django.db import transaction
from django.db.models import Q
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.exceptions import SheetNotFoundException, ValidationException
from api.utils.enum import ActionEnum, TableEnum, SwitchingTypeEnum
from api.utils.auditlog import AuditLog
from api.serializers import RealizationSerializer, SwitchingSerializer
from api.utils.excel import is_empty, export_errors_as_excel
from api.models import Realization, Switching
from django.db.models.base import ObjectDoesNotExist

from api.models import Coa, ProjectDetail, Budget, Planning
from api.utils import AuditLog

def update_db(request, index, data, errors):
    dcsp_id = data.pop('BID').split('-')[0]
    coa = get_coa(index, data.pop('COA'), errors)
    planning = get_planning(index, data.pop('Tahun'), errors)
    if planning != "planning-error":
        project_detail = get_project_detail(index, dcsp_id, planning, errors)
        if project_detail != 'project-detail-error' and coa != 'coa-error':
            budget_object = get_budget(index, project_detail, coa, errors)

    #If there's no error, then insert to DB
    if not errors:
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
                sw_in_data = Switching.objects.filter(to_plus = to_plus).filter(Q(type=SwitchingTypeEnum.SWITCH_IN.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_IN.value)).all()
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
                    type = SwitchingTypeEnum.SWITCH_IN.value
                
                '''If final_nominal is 0 (no changes on the nominal, dont create a new switching)'''
                if final_nominal:
                    switching = Switching.objects.create(
                        nominal = final_nominal,
                        to_plus = to_plus,
                        type = type
                    )
                    AuditLog.Save(SwitchingSerializer(switching).data, request, ActionEnum.CREATE.value, TableEnum.SWITCHING.value)
                    
            if switching_out:
                nominal = switching_out
                from_minus = budget_object
                #Get all data in switching
                sw_in_data = Switching.objects.filter(from_minus=from_minus).filter(Q(type=SwitchingTypeEnum.SWITCH_OUT.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_OUT.value)).all()
                total = 0
                for sw in sw_in_data:
                    total += sw.nominal
                if total > nominal:
                    final_nominal = nominal - total
                    type = SwitchingTypeEnum.CORRECTION_SWITCHING_OUT.value
                else:
                    final_nominal = nominal - total
                    type = SwitchingTypeEnum.SWITCH_OUT.value

                if final_nominal:
                    switching = Switching.objects.create(
                        nominal = final_nominal,
                        from_minus = from_minus,
                        type = type
                    )
                    AuditLog.Save(SwitchingSerializer(switching).data, request, ActionEnum.CREATE.value, TableEnum.SWITCHING.value)

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
                    AuditLog.Save(SwitchingSerializer(switching).data, request, ActionEnum.CREATE.value, TableEnum.SWITCHING.value)

            if topup:
                nominal = topup
                to_plus = budget_object
                #Get all data in switching
                sw_in_data = Switching.objects.filter(to_plus = to_plus).filter(Q(type=SwitchingTypeEnum.TOPUP.value)|Q(type=SwitchingTypeEnum.CORRECTION_TOPUP.value)).all()
                total = 0
                for sw in sw_in_data:
                    total += sw.nominal

                if total > nominal:
                    final_nominal = nominal - total
                    type = SwitchingTypeEnum.CORRECTION_TOPUP.value
                else:
                    final_nominal = nominal-total
                    type = SwitchingTypeEnum.TOPUP.value

                if final_nominal:
                    switching = Switching.objects.create(
                        nominal = final_nominal,
                        to_plus = to_plus,
                        type = type
                    )
                    AuditLog.Save(SwitchingSerializer(switching).data, request, ActionEnum.CREATE.value, TableEnum.SWITCHING.value)
        except TypeError:
            errors.append("Row {} - Wrong input type, number type input expected on collumn D afterward".format(index))

def get_coa(index, coa_name, errors):
    try:
        return Coa.objects.get(name=coa_name)
    except ObjectDoesNotExist:
        errors.append("Row {} - COA with name {} not found".format(index,coa_name))
        return "coa-error"
    
def get_project_detail(index, dcsp_id, planning, errors):
    try:
        return ProjectDetail.objects.filter(planning = planning).filter(dcsp_id = dcsp_id).get()
    except ObjectDoesNotExist:
        errors.append("Row {} - Project Detail with dcsp_id {} not found".format(index,dcsp_id))
        return "project-detail-error"

def get_planning(index, year, errors):
    try:
        return Planning.objects.filter(year = year).get()
    except ObjectDoesNotExist:
        errors.append("Row {} - Planning with year {} not found".format(index,year))
        return "planning-error"

def get_budget(index, project_detail, coa, errors):
    try:
        return Budget.objects.filter(project_detail=project_detail).filter(coa=coa).get()
    except ObjectDoesNotExist:
        errors.append("Row {} - Budget not found".format(index))
        return "budget-error"

def is_nan(data):
    return 0 if math.isnan(data) else data

class ImportRealisasi():
    parser_classes = (MultiPartParser, )

    #to validate empty inputs
    def validate_input(self, index, data):
        dcsp_id = data['BID']
        coa = data['COA']
        tahun = data['Tahun']
        errors = []

        if is_empty(dcsp_id):
            errors.append("Row {} - BID must be filled".format(index))
        if is_empty(coa):
            errors.append("Row {} - COA must be filled".format(index))
        if is_empty(tahun):
            errors.append("Row {} - Tahun must be filled".format(index))
        
        return errors

    @transaction.atomic
    def start(self, request):
        file_obj = request.FILES['file'].read()
        try:
            df = pandas.read_excel(file_obj, sheet_name='Realisasi')
        except ValueError:
            raise SheetNotFoundException('Realisasi')
        
        errors = []
        
        for index, row in df.iterrows():
            # Check for empties per row
            line_error = self.validate_input((index+2), row)
            errors.extend(line_error)
            if not line_error:
                update_db(request, (index+2), row, errors)

        if errors:
            export_errors_as_excel(errors)
        return Response(status=204)