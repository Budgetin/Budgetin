from rest_framework import viewsets
from api.models.monitoring_model import Monitoring
from api.serializers.monitoring_serializer import MonitoringSerializer
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.hit_api import get_biro_name

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum


class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    def list(self, request, *args, **kwargs):
        monitoring = super().list(request, *args, **kwargs)
        for each in monitoring.data:
            #each['biro_name'] = get_biro_name(each['biro_id'])
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return monitoring
    
    def retrieve(self, request, *args, **kwargs):
        monitoring = super().retrieve(request, *args, **kwargs)
        monitoring.data['created_at'] = timestamp_to_strdateformat(monitoring.data['created_at'], "%d %B %Y")
        monitoring.data['updated_at'] = timestamp_to_strdateformat(monitoring.data['updated_at'], "%d %B %Y")
        return monitoring

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        monitoring = super().create(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, ActionEnum.CREATE, TableEnum.MONITORING)
        return monitoring

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        monitoring = super().update(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, ActionEnum.UPDATE, TableEnum.MONITORING)
        return monitoring

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1                                 
        monitoring = super().destroy(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, ActionEnum.DELETE, TableEnum.MONITORING)
        return monitoring
