import datetime
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
