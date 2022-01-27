from rest_framework import viewsets
from api.models import MonitoringStatus
from api.serializers import MonitoringStatusSerializer

class MonitoringStatusViewSet(viewsets.ModelViewSet):
    queryset = MonitoringStatus.objects.all()
    serializer_class = MonitoringStatusSerializer
