from rest_framework import serializers

from api.models import Coa

class CoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coa
        fields = '__all__'

class CoaResponseSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    class Meta:
        model = Coa
        fields = '__all__'
        
    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.display_name
        return None

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.display_name
        return None
