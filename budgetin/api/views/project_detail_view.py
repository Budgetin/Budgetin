from rest_framework import viewsets
from api.models.project_detail_model import ProjectDetail
from api.serializers.project_detail_serializer import ProjectDetailSerializer


class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer
