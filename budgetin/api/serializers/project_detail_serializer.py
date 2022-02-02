from rest_framework import serializers

from api.models import ProjectDetail, Planning, Project, Product, Strategy, Biro, ProjectType
from api.serializers import BudgetResponseSerializer


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = '__all__'
        
