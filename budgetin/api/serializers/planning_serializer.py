from rest_framework import serializers

from api.models import Planning

class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = '__all__'
        
class PlanningResponseSerializer(serializers.ModelSerializer):
    is_active = serializers.IntegerField()
    notification = serializers.IntegerField()
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Planning
        fields = '__all__'
