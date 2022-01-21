import datetime
from rest_framework import viewsets
from api.models.monitoring_model import Monitoring
from api.serializers.monitoring_serializer import MonitoringSerializer
from api.models.audit_log_model import AuditLog

class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    def create(self, request, *args, **kwargs):
        monitoring = super().create(request, *args, **kwargs)
        serial_data = {
            "name": monitoring.data['name'],
            "definition": monitoring.data['definition'],
            "hyperion_name": monitoring.data['hyperion_name'],
        }
        AuditLog.objects.create(timestamp=datetime.datetime.now(
        ), modified_by=request.custom_user['id'], entity_id=monitoring.data['id'], serialized_data=serial_data, action_id_id=1, table_id_id=4)
        return monitoring

    def update(self, request, *args, **kwargs):
        monitoring_update = super().update(request, *args, **kwargs)
        AuditLog.objects.create(timestamp=datetime.datetime.now(
        ), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data=request.data, action_id_id=3, table_id_id=4)
        return monitoring_update

    def destroy(self, request, *args, **kwargs):
        monitoring_destroy = super().destroy(request, *args, **kwargs)
        AuditLog.objects.create(timestamp=datetime.datetime.now(), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data={
                                "data": "destroyed"}, action_id_id=4, table_id_id=4)
        return monitoring_destroy