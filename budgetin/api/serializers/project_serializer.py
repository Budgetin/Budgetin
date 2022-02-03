from rest_framework import serializers

from api.models import Project, Product, Biro, ProjectDetail, Planning, Budget

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    strategy = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'product_name', 'product_code', 'strategy']
        
    def get_strategy(self, product):
        return product.strategy.name
        
class BiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biro
        fields = ['id', 'rcc', 'code', 'name' ]

class PlanningSerializer(serializers.ModelSerializer):
    due_date = serializers.SerializerMethodField()
    class Meta:
        model = Planning
        fields = ['id', 'year', 'is_active', 'due_date']

    def get_due_date(self, planning):
        return planning.due_date.strftime("%d %B %Y")
        
class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        exclude = ['is_deleted', 'deleted_at', 'created_at', 'updated_at', 'created_by', 'updated_by']
        

class ProjectDetailSerializer(serializers.ModelSerializer):
    project_type = serializers.SerializerMethodField()
    planning = PlanningSerializer()
    budget = BudgetSerializer(many=True)
    
    class Meta:
        model = ProjectDetail
        fields = ['id', 'dcsp_id', 'project_type', 'planning', 'budget']
        
    def get_project_type(self, project_detail):
        return project_detail.project_type.name

class ProjectResponseSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False)
    biro = BiroSerializer(many=False)
    project_detail = ProjectDetailSerializer(many=True)
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Project
        fields = ['id', 'created_by', 'updated_by', 'created_at', 'updated_at', 'itfam_id', 'project_name', 'project_description', 'start_year', 'end_year', 'is_tech', 'total_investment_value', 'biro', 'product', 'project_detail']
