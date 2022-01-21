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
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, AuditLog.Create, AuditLog.Coa)
        # AuditLog.objects.create(timestamp=datetime.datetime.now(
        # ), modified_by=request.custom_user['id'], entity_id=coa.data['id'], serialized_data=coa.data, action_id_id=1, table_id_id=4)
        return coa

    def update(self, request, *args, **kwargs):
        coa = super().update(request, *args, **kwargs)
        AuditLog.Save(coa, request, AuditLog.Update, AuditLog.Coa)
        # AuditLog.objects.create(timestamp=datetime.datetime.now(
        # ), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data=coa_update.data, action_id_id=3, table_id_id=4)
        return coa

    def destroy(self, request, *args, **kwargs):
        coa = super().destroy(request, *args, **kwargs)
        AuditLog.Save(coa, request, AuditLog.Delete, AuditLog.Coa)
        #AuditLog.Save(coa, request, AuditLog.Delete, AuditLog.Coa)
        # AuditLog.objects.create(timestamp=datetime.datetime.now(), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data={
        #                         "data": "destroyed"}, action_id_id=4, table_id_id=4)
        return coa
