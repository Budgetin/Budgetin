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
        return product.strategy.name
        
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
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Budget
        fields = ['id', 'is_budget', 'expense_type', 'planning_nominal', 'planning_q1', 'planning_q2', 'planning_q3', 'planning_q4', 
                  'realization_jan', 'realization_feb', 'realization_mar', 'realization_apr', 'realization_may',
                  'realization_jun', 'realization_jul', 'realization_aug', 'realization_sep', 'realization_oct',
                  'realization_nov', 'realization_dec', 'switching_in', 'switching_out', 'top_up', 'returns',
                  'allocate', 'coa', 'project_detail', 'created_by', 'updated_by', 'created_at', 'updated_at']
        
    def get_coa(self, budget):
        return budget.coa.name
    
    def get_planning_nominal(self, budget):
        return budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4
    
    def get_is_budget(self, budget):
        return 1 if budget.expense_type != "" else 0