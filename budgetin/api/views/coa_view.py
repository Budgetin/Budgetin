from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from api.models import Coa, User
from api.serializers import CoaSerializer, CoaResponseSerializer
from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum,TableEnum
from api.utils.file import read_file, get_import_template_path, load_file
from api.utils.excel import read_excel, remove_sheet, export_excel, is_empty, export_errors_as_excel
from api.exceptions import ValidationException

def is_duplicate_coa_create(name, hyperion_name):
    if Coa.objects.filter(name__iexact=name):
        raise ValidationException('COA ' + name + ' already exists')
    if Coa.objects.filter(hyperion_name__iexact=hyperion_name):
        raise ValidationException('COA with hyperion name ' + hyperion_name + ' already exists')

def is_duplicate_coa(id, name, hyperion_name):
    if Coa.objects.filter(name__iexact=name).exclude(id=id):
        raise ValidationException('COA ' + name + ' already exists')
    if Coa.objects.filter(hyperion_name__iexact=hyperion_name).exclude(id=id):
        raise ValidationException('COA with hyperion name ' + hyperion_name + ' already exists')
class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Coa.objects.select_related('updated_by', 'created_by').all()
        for coa in queryset:
            coa.format_timestamp("%d %B %Y")
            
        serializer = CoaResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        coa =  Coa.objects.select_related('updated_by', 'created_by').get(pk=kwargs['pk'])
        coa.format_timestamp("%d %B %Y")
        
        serializer = CoaResponseSerializer(coa, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.custom_user['id']
        request.data['updated_by'] = request.custom_user['id']
        request.data['name'] = request.data['name'].strip()
        request.data['hyperion_name'] = request.data['hyperion_name'].strip()
        is_duplicate_coa_create(request.data['name'],request.data['hyperion_name'])
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.CREATE, TableEnum.COA)
        return coa

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['name'] = request.data['name'].strip()
        request.data['hyperion_name'] = request.data['hyperion_name'].strip()
        is_duplicate_coa(kwargs['pk'],request.data['name'],request.data['hyperion_name'])
        coa = super().update(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.UPDATE, TableEnum.COA)
        return coa

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        coa = super().destroy(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.DELETE, TableEnum.COA)
        return coa
    
    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='import')
    def import_from_excel(self, request):
        file = read_file(request)
        df = read_excel(file, TableEnum.COA.value)
        errors = []
        
        for index, data in df.iterrows():
            errors = self.insert_to_db(request, data, (index+2), errors)
        
        if errors:            
            return export_errors_as_excel(errors)
        
        return Response(status=204)
    
    def insert_to_db(self, request, data, index, errors):
        errors.extend(self.validate_data(data, index))

        if not errors:
            self.create_or_update_coa(request, data)

        return errors
    
    def validate_data(self, data, index):
        errors = []
        errors = self.validate_coa(data, index, errors)
        return errors
    
    def validate_coa(self, data, index, errors):
        name = data['coa_name']
        is_capex = data['is_capex']
        minimum_item_origin = data['minimum_item_origin']
        
        if is_empty(name):
            errors.append("Row {} - Coa name must be filled".format(index))
        if not is_empty(is_capex) and is_capex.lower() == 'yes' and is_empty(minimum_item_origin):
            errors.append("Row {} - Minimum item origin must be filled if COA can be considered as capex".format(index))
            
        return errors
    
    def create_or_update_coa(self, request, data):
        update_dict = {
            'definition': data['coa_definition'] if not is_empty(data['coa_definition']) else None,
            'hyperion_name': data['hyperion_name'] if not is_empty(data['hyperion_name']) else None,
            'is_capex': True if not is_empty(data['is_capex']) and data['is_capex'].lower() == 'yes' else False,
            'minimum_item_origin': data['minimum_item_origin'] if not is_empty(data['minimum_item_origin']) else None,
            'updated_by': User.objects.get(pk=request.custom_user['id'])
        }
        
        coa = Coa.objects.filter(name=data['coa_name']).first()
        new_coa = Coa(
            name = data['coa_name'],
            **update_dict
        )
        
        if not coa:
            self.create_new_coa(request, new_coa)
        elif coa and not coa.equal(new_coa):
            self.update_coa(request, coa, update_dict)
            
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
    
    @action(methods=['get'], detail=False, url_path='import/template')
    def download_import_template(self, request):
        file_path = get_import_template_path(TableEnum.COA)
        file = load_file(file_path, 'rb')
        
        return export_excel(file, 'import_template_strategy.xlsx')