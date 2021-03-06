from math import fabs
from rest_framework import serializers

from api.models import Budget, Product, Biro, Project, ProjectDetail, Planning


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    strategy = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'product_code', 'strategy']
        
    def get_strategy(self, product):
        if product.strategy:
            return product.strategy.name
        
class BiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biro
        fields = ['id', 'code', 'name', 'rcc']

class ProjectSerializer(serializers.ModelSerializer):
    is_tech = serializers.SerializerMethodField()
    product = ProductSerializer(many=False)
    biro = BiroSerializer(many=False)
    class Meta:
        model = Project
        fields = ['id', 'project_name', 'project_description', 'itfam_id', 'is_tech', 'start_year', 'end_year', 'total_investment_value', 'product', 'biro']
        
    def get_is_tech(self, project):
        return 1 if project.is_tech == True else 0

class PlanningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planning
        fields = ['id', 'year', 'due_date', 'is_active']

class ProjectDetailSerializer(serializers.ModelSerializer):
    planning = PlanningSerializer(many=False)
    project = ProjectSerializer(many=False)
    project_type = serializers.SerializerMethodField()
    class Meta:
        model = ProjectDetail
        fields = ['id', 'dcsp_id', 'planning', 'project', 'project_type']
        
    def get_project_type(self, project_detail):
        return project_detail.project_type.name


class BudgetResponseSerializer(serializers.ModelSerializer):
    coa = serializers.SerializerMethodField()
    planning_nominal = serializers.SerializerMethodField()
    is_budget = serializers.SerializerMethodField()
    project_detail = ProjectDetailSerializer()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    class Meta:
        model = Budget
        fields = ['id', 'is_budget', 'expense_type', 'planning_nominal', 'planning_q1', 'planning_q2', 'planning_q3', 'planning_q4',
                  'allocate', 'coa', 'project_detail', 'created_by', 'updated_by', 'is_active', 'created_at', 'updated_at']
        
    def get_coa(self, budget):
        if budget.coa:
            return budget.coa.name
        return None

    def get_planning_nominal(self, budget):
        return budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4
    
    def get_is_budget(self, budget):
        return 1 if budget.expense_type != "" else 0

    def get_created_by(self, budget):
        if budget.created_by:
            return budget.created_by.display_name
        return None

    def get_updated_by(self, budget):
        if budget.updated_by:
            return budget.updated_by.display_name
        return None