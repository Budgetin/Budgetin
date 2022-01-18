from rest_framework import serializers
from api.models.project_type_model import ProjectType


class ProjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectType
        fields = '__all__'
