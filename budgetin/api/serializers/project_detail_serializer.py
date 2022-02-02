from rest_framework import serializers

from api.models import ProjectDetail, Planning, Project, Product, Strategy, Biro, ProjectType
from api.serializers import BudgetResponseSerializer


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = '__all__'
        
class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = '__all__'

class StrategySerializer(serializers.ModelSerializer):
    class Meta:
        model = Strategy
        fields = '__all__'
class ProductSerializer(serializers.ModelSerializer):
    strategy = StrategySerializer(many=False)
    class Meta:
        model = Product
        fields = ['id', 'product_code', 'strategy']
        
class BiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biro
        fields = ['id', 'code', 'name', 'rcc']

class ProjectSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    biro = BiroSerializer(many=False)
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_description', 'itfam_id', 'is_tech', 'start_year', 'end_year', 'total_investment_value', 'product', 'biro']
        
class ProjectDetailResponseSerializer(serializers.ModelSerializer):
    planning = PlanningSerializer(many=False)
    project = ProjectSerializer(many=False)
    budget = BudgetResponseSerializer(many=True)
    project_type_name = serializers.CharField()
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = ProjectDetail
        fields = ['id', 'dcsp_id', 'project_type_name', 'project', 'planning', 'budget', 'is_deleted', 'deleted_at', 'created_at', 'updated_at', 'created_by', 'updated_by']
