from rest_framework import serializers

from api.models import Monitoring


class MonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoring
        fields = '__all__'
