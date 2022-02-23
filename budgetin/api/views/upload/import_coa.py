from rest_framework.response import Response

from api.models import Coa, User
from api.serializers import CoaSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum,TableEnum
from api.utils.file import read_file
from api.utils.excel import read_excel, is_empty, export_errors_as_excel

class ImportCoa():
    def start(self, request):
        file = read_file(request)
        df = read_excel(file, TableEnum.COA.value)
        errors = []
        
        '''
            Retrieve data from DB and convert it to Key, Value dictionary.
            This is done to reduce DB calls and optimize searching for specified key with O(1) complexity when searching 
            e.g{'hw': Coa (obj), 'm.hw': Coa (obj)}
        '''
        coas = dict((coa.name.lower(), coa) for coa in Coa.objects.all())
        
        for index, data in df.iterrows():
            errors = self.validate_coa(data, index+2, errors)
            errors = self.validate_minimum_item_origin(data, index+2, errors)
            
            if not errors:
                coas = self.create_or_update_coa(request, coas, data)
        
        if errors:            
            return export_errors_as_excel(errors)
        
        return Response(status=204)
    
    def validate_coa(self, data, index, errors):
        name = data['coa_name']
        
        if is_empty(name):
            errors.append("Row {} - Coa name must be filled".format(index))
        return errors
    
    def validate_minimum_item_origin(self, data, index, errors):
        is_capex = data['is_capex']
        minimum_item_origin = data['minimum_item_origin']
        
        if not is_empty(is_capex) and is_capex.lower() == 'yes' and is_empty(minimum_item_origin):
            errors.append("Row {} - Minimum item origin must be filled if COA can be considered as capex".format(index))
        return errors
    
    def create_or_update_coa(self, request, coas, data):
        update_dict = {
            'definition': data['coa_definition'] if not is_empty(data['coa_definition']) else None,
            'hyperion_name': data['hyperion_name'] if not is_empty(data['hyperion_name']) else None,
            'is_capex': True if not is_empty(data['is_capex']) and data['is_capex'].lower() == 'yes' else False,
            'minimum_item_origin': data['minimum_item_origin'] if not is_empty(data['minimum_item_origin']) else None,
            'updated_by': User.objects.get(pk=request.custom_user['id'])
        }
        
        coa_name = data['coa_name'].strip()
        new_coa = Coa(
            name = coa_name,
            **update_dict
        )
        
        if coa_name.lower() not in coas:
            coa = self.create_new_coa(request, new_coa)
        else:
            coa = coas[coa_name.lower()]
            if not coa.equal(new_coa):
                coa = self.update_coa(request, coa, update_dict)
            
        coas[coa_name] = coa
        return coas
            
    def create_new_coa(self, request, new_coa):
        new_coa.created_by = new_coa.updated_by
        new_coa.save()
        AuditLog.Save(CoaSerializer(new_coa), request, ActionEnum.CREATE, TableEnum.COA) 

    def update_coa(self, request, coa, update_dict):
        coa = self.update_fields(coa, update_dict)
        coa.save()
        AuditLog.Save(CoaSerializer(coa), request, ActionEnum.UPDATE, TableEnum.COA) 

    def update_fields(self, model, update_dict):
        for key, value in update_dict.items():
            setattr(model, key, value)
        return model