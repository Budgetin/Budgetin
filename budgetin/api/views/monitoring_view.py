from rest_framework import viewsets
from api.models.monitoring_model import Monitoring
from api.serializers.monitoring_serializer import MonitoringSerializer
from datetime import datetime

#For Audit Logging
from api.utils.auditlog import AuditLog

class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    def list(self, request, *args, **kwargs):
        monitoring = super().list(request, *args, **kwargs)
        for each in monitoring.data:
            createdDate = each['created_at']
            date_time_obj = datetime.fromisoformat(createdDate)
            each['created_at'] = date_time_obj.strftime("%d %B %Y")

            updatedDate = each['updated_at']
            date_time_obj = datetime.fromisoformat(updatedDate)
            each['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return monitoring
    
    def retrieve(self, request, *args, **kwargs):
        monitoring = super().retrieve(request, *args, **kwargs)
        createdDate = monitoring.data['created_at']
        date_time_obj = datetime.fromisoformat(createdDate)
        monitoring.data['created_at'] = date_time_obj.strftime("%d %B %Y")

        updatedDate = monitoring.data['updated_at']
        date_time_obj = datetime.fromisoformat(updatedDate)
        monitoring.data['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return monitoring

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        monitoring = super().create(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, AuditLog.Create, AuditLog.Monitoring)
        return monitoring

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        monitoring = super().update(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, AuditLog.Update, AuditLog.Monitoring)
        return monitoring

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        monitoring = super().destroy(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, AuditLog.Delete, AuditLog.Monitoring)
        return monitoring
