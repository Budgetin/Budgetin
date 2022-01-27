from django.forms.models import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response


from api.models import Monitoring
from api.serializers import MonitoringSerializer
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

def construct_monitoring_dict(monitoring):
    monitoring_dict = model_to_dict(monitoring)
    monitoring_dict['biro'] = model_to_dict(monitoring.biro)
    monitoring_dict['status'] = monitoring.monitoring_status.name
    monitoring_dict['created_at'] = monitoring.created_at.strftime("%d %B %Y")
    monitoring_dict['updated_at'] = monitoring.updated_at.strftime("%d %B %Y")
    return monitoring_dict

class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer

    def list(self, request, *args, **kwargs):
        parameter  = request.GET.get('planning')
        if parameter:
            monitoring = Monitoring.objects.select_related('biro').select_related('monitoring_status').filter(planning=parameter)
        else:
            monitoring = Monitoring.objects.select_related('biro').select_related('monitoring_status').all()

        result = []
        for each in monitoring:
            each_dict = construct_monitoring_dict(each)
            result.append(each_dict)
        return Response(result)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        monitoring = Monitoring.objects.select_related('biro').select_related('monitoring_status').get(pk=id)
        monitoring_dict = construct_monitoring_dict(monitoring)
        return Response(monitoring_dict)

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
