from rest_framework import serializers
from api.models.projectDetail_model import ProjectDetail


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = '__all__'
