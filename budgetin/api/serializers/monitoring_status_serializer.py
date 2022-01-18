from rest_framework import serializers
from api.models.monitoring_status_model import MonitoringStatus


class MonitoringStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonitoringStatus
        fields = '__all__'
