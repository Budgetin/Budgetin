from rest_framework import serializers

from api.models import ProjectDetail, Planning, Project, Product, Strategy, Biro, ProjectType
from api.serializers import PlanningResponseSerializer


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = '__all__'
        
class ProjectDetailResponseSerializer(serializers.ModelSerializer):
    project_type = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()
    updated_by = serializers.SerializerMethodField()
    planning = PlanningResponseSerializer(many=False)
    class Meta:
        model = ProjectDetail
        fields = ['id', 'dcsp_id', 'project_type', 'is_deleted', 'deleted_at', 'created_at', 'updated_at', 
        'created_by', 'updated_by', 'planning', 'project']
        
    def get_project_type(self, project_detail):
        return project_detail.project_type.name
    
    def get_created_by(self, obj):
        if obj.created_by:
            return obj.created_by.display_name
        return None

    def get_updated_by(self, obj):
        if obj.updated_by:
            return obj.updated_by.display_name
        return None
        
