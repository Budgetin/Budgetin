from rest_framework import viewsets
from api.models.monitoring_status_model import MonitoringStatus
from api.serializers.monitoring_status_serializer import MonitoringStatusSerializer


class MonitoringStatusViewSet(viewsets.ModelViewSet):
    queryset = MonitoringStatus.objects.all()
    serializer_class = MonitoringStatusSerializer
