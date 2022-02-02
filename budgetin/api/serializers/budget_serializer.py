from rest_framework import serializers

from api.models import Budget, Product, Biro, Project, ProjectDetail


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
        
class ProjectDetailSerializer(serializers.ModelSerializer):
    year = serializers.SerializerMethodField()
    project = ProjectSerializer(many=False)
    class Meta:
        model = ProjectDetail
        fields = ['id', 'dcsp_id', 'year', 'project']
    def get_year(self, project_detail):
        return project_detail.planning.year

class BudgetResponseSerializer(serializers.ModelSerializer):
    coa = serializers.SerializerMethodField()
    project_detail = ProjectDetailSerializer()
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Budget
        fields = ['id', 'expense_type', 'planning_q1', 'planning_q2', 'planning_q3', 'planning_q4', 
                  'realization_jan', 'realization_feb', 'realization_mar', 'realization_apr', 'realization_may',
                  'realization_jun', 'realization_jul', 'realization_aug', 'realization_sep', 'realization_oct',
                  'realization_nov', 'realization_dec', 'switching_in', 'switching_out', 'top_up', 'returns',
                  'allocate', 'coa', 'project_detail', 'created_by', 'updated_by']
        
    def get_coa(self, budget):
        return budget.coa.name