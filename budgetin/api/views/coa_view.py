from datetime import datetime
from rest_framework import viewsets
from api.models.coa_model import Coa
from api.serializers.coa_serializer import CoaSerializer
from api.permissions import IsAuthenticated, IsAdmin

#For Audit Logging
from api.utils.auditlog import AuditLog

class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
    # permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        coa = super().list(request, *args, **kwargs)
        for each in coa.data:
            createdDate = each['created_at']
            date_time_obj = datetime.fromisoformat(createdDate)
            each['created_at'] = date_time_obj.strftime("%d %B %Y")

            updatedDate = each['updated_at']
            date_time_obj = datetime.fromisoformat(updatedDate)
            each['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return coa
    
    def retrieve(self, request, *args, **kwargs):
        coa = super().retrieve(request, *args, **kwargs)
        createdDate = coa.data['created_at']
        date_time_obj = datetime.fromisoformat(createdDate)
        coa.data['created_at'] = date_time_obj.strftime("%d %B %Y")

        updatedDate = coa.data['updated_at']
        date_time_obj = datetime.fromisoformat(updatedDate)
        coa.data['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return coa

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, AuditLog.Create, AuditLog.Coa)
        return coa

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        coa = super().update(request, *args, **kwargs)
        AuditLog.Save(coa, request, AuditLog.Update, AuditLog.Coa)
        return coa

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        coa = super().destroy(request, *args, **kwargs)
        AuditLog.Save(coa, request, AuditLog.Delete, AuditLog.Coa)
        return coa
