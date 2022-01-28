from rest_framework import viewsets

from api.models import Coa, User
from api.serializers import CoaSerializer
from api.permissions import IsAuthenticated, IsAdmin
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum,TableEnum
from api.exceptions.validation_exception import ValidationException

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
        coa = super().list(request, *args, **kwargs)
        for each in coa.data:
            if each['updated_by'] is not None:
                each['updated_by'] = User.all_objects.get(pk=each['updated_by']).display_name
            else:
                each['updated_by'] = ''
            each['created_by'] = User.all_objects.get(pk=each['created_by']).display_name
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return coa
    
    def retrieve(self, request, *args, **kwargs):
        coa = super().retrieve(request, *args, **kwargs)
        if coa.data['updated_by'] is not None:
                coa.data['updated_by'] = User.all_objects.get(pk=coa.data['updated_by']).display_name
        else:
            coa.data['updated_by'] = ''
        coa.data['created_by'] = User.all_objects.get(pk=coa.data['created_by']).display_name
        coa.data['created_at'] = timestamp_to_strdateformat(coa.data['created_at'], "%d %B %Y")
        coa.data['updated_at'] = timestamp_to_strdateformat(coa.data['updated_at'], "%d %B %Y")
        
        return coa

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        is_duplicate_coa_create(request.data['name'],request.data['hyperion_name'])
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.CREATE, TableEnum.COA)
        return coa

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        is_duplicate_coa(kwargs['id'],request.data['name'],request.data['hyperion_name'])
        coa = super().update(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.UPDATE, TableEnum.COA)
        return coa

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        coa = super().destroy(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.DELETE, TableEnum.COA)
        return coa
