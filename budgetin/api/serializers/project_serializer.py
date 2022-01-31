from rest_framework import serializers

from api.models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'

class ProjectResponseSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Project
        fields = '__all__'
