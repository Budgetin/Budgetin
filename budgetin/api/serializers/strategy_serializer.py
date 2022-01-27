from rest_framework import serializers

from api.models import Strategy
class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = '__all__'