import pandas as pd
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from api.models import Coa
from api.serializers import CoaSerializer, CoaResponseSerializer
from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum,TableEnum
from api.utils.file import read_excel
from api.exceptions import ValidationException

def is_duplicate_coa_create(name, hyperion_name):
    if Coa.objects.filter(name=name) or Coa.objects.filter(hyperion_name=hyperion_name):
        raise ValidationException('COA ' + name + ' already exists')

def is_duplicate_coa(id, name, hyperion_name):
    if Coa.objects.filter(name=name).exclude(id=id) or Coa.objects.filter(hyperion_name=hyperion_name).exclude(id=id):
        raise ValidationException('COA ' + name + ' already exists')
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
        is_duplicate_coa_create(request.data['name'],request.data['hyperion_name'])
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.CREATE, TableEnum.COA)
        return coa

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
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
        file = request.FILES['file'].read()
        df = read_excel(file, 'coa')
        errors = []
        
        for index, row in df.iterrows():
            errors.extend(self.insert_to_db(request, row, (index+2)))
        
        if errors:
            raise ValidationException(errors)
        
        return Response(status=204)
    
    def insert_to_db(self, request, data, index):
        errors = []
        
        name = data['coa_name']
        errors = self.validate_coa(name, index, errors)

        if not errors:
            coa = self.create_coa(request, data)
            AuditLog.Save(CoaSerializer(coa), request, ActionEnum.CREATE, TableEnum.COA) 

        return errors
    
    def validate_coa(self, name, index, errors):
        if pd.isnull(name):
            errors.append("Coa name must be filled at line {}".format(index))
        elif self.coa_already_exists(name):
            errors.append("Coa '{}' at line {} already exists".format(name, index))
        return errors
            
    def coa_already_exists(self, name):
        return Coa.objects.filter(name__iexact=name).count() > 0
    
    def create_coa(self, request, data):
        return Coa.objects.create(
            name = data['coa_name'],
            definition = data['coa_definition'] if not pd.isnull(data['coa_definition']) else None,
            hyperion_name = data['hyperion_name'] if not pd.isnull(data['hyperion_name']) else None,
            is_capex = True,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )