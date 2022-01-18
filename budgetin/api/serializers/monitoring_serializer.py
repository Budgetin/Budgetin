from rest_framework import serializers
from api.models.monitoring_model import Monitoring


class MonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoring
        fields = '__all__'
