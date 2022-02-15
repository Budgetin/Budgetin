from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Monitoring
from api.serializers import MonitoringSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum, MonitoringStatusEnum
from api.permissions import IsAuthenticated, IsAdmin

class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        planning  = request.GET.get('planning')
        if planning:
            queryset = Monitoring.objects.select_related('biro', 'planning').filter(planning=planning)
        else:
            queryset = Monitoring.objects.select_related('biro', 'planning').all()

        queryset.filter(~Q(monitoring_status=MonitoringStatusEnum.OPTIONAL.value))
        for monitoring in queryset:
            monitoring.format_timestamp("%d %B %Y")

        serializer = MonitoringSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        monitoring = Monitoring.objects.select_related('biro', 'planning').get(pk=id)
        
        serializer = MonitoringSerializer(monitoring, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        monitoring = super().create(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, ActionEnum.CREATE, TableEnum.MONITORING)
        return monitoring

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        monitoring = super().update(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, ActionEnum.UPDATE, TableEnum.MONITORING)
        return monitoring

    def destroy(self, request, *args, **kwargs):
        return Response({
            'message': 'Monitoring cannot be deleted'
        })
