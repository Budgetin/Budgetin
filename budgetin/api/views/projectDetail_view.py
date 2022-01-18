from rest_framework import viewsets
from api.models.projectDetail_model import ProjectDetail
from api.serializers.projectDetail_serializer import ProjectDetailSerializer


class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer
