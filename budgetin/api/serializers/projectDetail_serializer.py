from rest_framework import serializers
from models.projectDetail_model import ProjectDetail


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectDetail
        fields = '__all__'
