from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Coa
from api.serializers import CoaSerializer, CoaResponseSerializer
from api.permissions import IsAuthenticated, IsAdmin
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum,TableEnum
from api.exceptions import ValidationException

def is_duplicate_coa_create(name, hyperion_name):
    if Coa.objects.filter(name=name).exclude(hyperion_name=hyperion_name) or Coa.objects.filter(hyperion_name=hyperion_name).exclude(name=name):
        raise ValidationException

def is_duplicate_coa(id, name, hyperion_name):
    if Coa.objects.filter(name=name).exclude(id=id) or Coa.objects.filter(hyperion_name=hyperion_name).exclude(id=id):
        raise ValidationException
class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Coa.objects.all()
        for coa in queryset:
            coa.format_timestamp("%d %B %Y")
            coa.format_created_updated_by()
            
        serializer = CoaResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        coa =  Coa.objects.get(pk=kwargs['pk'])
        coa.format_timestamp("%d %B %Y")
        coa.format_created_updated_by()
        
        serializer = CoaResponseSerializer(coa, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        is_duplicate_coa_create(request.data['name'],request.data['hyperion_name'])
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.CREATE, TableEnum.COA)
        return coa

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        is_duplicate_coa(kwargs['pk'],request.data['name'],request.data['hyperion_name'])
        coa = super().update(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.UPDATE, TableEnum.COA)
        return coa

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        coa = super().destroy(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.DELETE, TableEnum.COA)
        return coa
