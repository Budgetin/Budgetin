from rest_framework import serializers

from api.models import ProjectDetail, Planning, Project, Product, Strategy, Biro, ProjectType
from api.serializers import BudgetResponseSerializer


class ProjectDetailSerializer(serializers.ModelSerializer):
    project_type = serializers.SerializerMethodField()
    class Meta:
        model = ProjectDetail
        fields = '__all__'
        
    def get_project_type(self, project_detail):
        return project_detail.project_type.name
        
