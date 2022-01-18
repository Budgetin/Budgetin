from rest_framework import viewsets
from api.models.project_model import Project
from api.serializers.project_serializer import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
