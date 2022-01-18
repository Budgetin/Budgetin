from rest_framework import viewsets
from models.projectDetail_model import ProjectDetail
from serializers.projectDetail_serializer import ProjectDetailSerializer


class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer
