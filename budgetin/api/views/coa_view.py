import datetime
from rest_framework import viewsets
from api.models.coa_model import Coa
from api.models.audit_log_model import AuditLog
from api.serializers.coa_serializer import CoaSerializer
from api.permissions import IsAuthenticated, IsAdmin


class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        coa = super().create(request, *args, **kwargs)
        serial_data = {
            "name": coa.data['name'],
            "definition": coa.data['definition'],
            "hyperion_name": coa.data['hyperion_name'],
        }
        AuditLog.objects.create(timestamp=datetime.datetime.now(
        ), modified_by=request.custom_user['id'], entity_id=coa.data['id'], serialized_data=serial_data, action_id_id=1, table_id_id=4)
        return coa

    def update(self, request, *args, **kwargs):
        coa_update = super().update(request, *args, **kwargs)
        AuditLog.objects.create(timestamp=datetime.datetime.now(
        ), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data=request.data, action_id_id=3, table_id_id=4)
        return coa_update

    def destroy(self, request, *args, **kwargs):
        coa_destroy = super().destroy(request, *args, **kwargs)
        AuditLog.objects.create(timestamp=datetime.datetime.now(), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data={
                                "data": "destroyed"}, action_id_id=4, table_id_id=4)
        return coa_destroy
