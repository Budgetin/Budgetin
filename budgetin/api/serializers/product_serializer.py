from rest_framework import serializers

from api.models import Product
from api.models import Strategy

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = ['id', 'name']
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'                
        
class ProductResponseSerializer(serializers.ModelSerializer):
    strategy = StrategySerializer(many=False)
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Product
        fields = ['id', 'product_code', 'product_name', 'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by', 'strategy']        