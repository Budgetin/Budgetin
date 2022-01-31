from rest_framework import serializers

from api.models import Strategy
class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = '__all__'
        
class StrategyResponseSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Strategy
        fields = '__all__'