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
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()

    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.display_name
        return None

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.display_name
        return None
    class Meta:
        model = Product
        fields = ['id', 'product_code', 'product_name', 'is_active', 'created_at', 'updated_at', 'created_by', 'updated_by', 'strategy']        