from rest_framework import serializers

from api.models import Project
from api.serializers import ProductSerializer, BiroSerializer

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectResponseSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    biro = BiroSerializer(many=False)
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Project
        fields = ['id', 'created_by', 'updated_by', 'is_deleted', 'deleted_at', 'created_at', 'updated_at', 'itfam_id', 'project_name', 'project_description', 'start_year', 'end_year', 'total_investment_value', 'is_tech', 'biro', 'product']
