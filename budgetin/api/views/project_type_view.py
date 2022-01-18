from rest_framework import viewsets
from api.models.project_type_model import ProjectType
from api.serializers.project_type_serializer import ProjectTypeSerializer


class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
