import datetime
from rest_framework import serializers

from api.models import Monitoring, Biro, Planning
class MonitoringBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Monitoring
        fields = '__all__'
class BiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biro
        fields = ['id', 'code', 'sub_group_code', 'group_code']
        
class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = ['id', 'year', 'is_active']
        
class MonitoringSerializer(serializers.ModelSerializer):
    biro = BiroSerializer(many=False)
    planning = PlanningSerializer(many=False)
    due_date = serializers.SerializerMethodField()
    class Meta:
        model = Monitoring
        fields = ['id', 'pic_employee_id', 'pic_initial', 'pic_display_name', 'monitoring_status', 'biro', 'planning', 'due_date', 'updated_at']

    def get_due_date(self, monitoring):
        return monitoring.planning.due_date.strftime("%d %B %Y")