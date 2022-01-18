from rest_framework import viewsets
from api.models.monitoring_model import Monitoring
from api.serializers.monitoring_serializer import MonitoringSerializer


class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
