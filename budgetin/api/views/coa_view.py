from rest_framework import viewsets
from api.models.coa_model import Coa
from api.serializers.coa_serializer import CoaSerializer
from api.permissions import IsAuthenticated, IsAdmin
from api.utils.date_format import timestamp_to_strdateformat

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum,TableEnum

class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        coa = super().list(request, *args, **kwargs)
        for each in coa.data:
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return coa
    
    def retrieve(self, request, *args, **kwargs):
        coa = super().retrieve(request, *args, **kwargs)
        coa.data['created_at'] = timestamp_to_strdateformat(coa.data['created_at'], "%d %B %Y")
        coa.data['updated_at'] = timestamp_to_strdateformat(coa.data['updated_at'], "%d %B %Y")
        
        return coa

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.CREATE, TableEnum.COA)
        return coa

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        coa = super().update(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.UPDATE, TableEnum.COA)
        return coa

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        coa = super().destroy(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.DELETE, TableEnum.COA)
        return coa
