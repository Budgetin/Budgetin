from rest_framework import serializers

from api.models import Planning

class ActivePlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = ['id', 'year']

class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = '__all__'
        
class PlanningResponseSerializer(serializers.ModelSerializer):
    is_active = serializers.IntegerField()
    notification = serializers.IntegerField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    class Meta:
        model = Planning
        fields = '__all__'
        
    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.display_name
        return None

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.display_name
        return None
