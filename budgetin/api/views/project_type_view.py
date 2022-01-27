from rest_framework import viewsets

from api.models import ProjectType
from api.serializers import ProjectTypeSerializer

class ProjectTypeViewSet(viewsets.ModelViewSet):
    queryset = ProjectType.objects.all()
    serializer_class = ProjectTypeSerializer
