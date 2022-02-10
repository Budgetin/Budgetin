from rest_framework import viewsets
from rest_framework.response import Response

from api.models.project_detail_model import ProjectDetail
from api.serializers import ProjectDetailSerializer, ProjectDetailResponseSerializer

from api.models import ProjectDetail
from api.serializers import ProjectDetailSerializer
from api.permissions import IsAuthenticated, IsAdmin
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum


class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        queryset = ProjectDetail.objects.select_related('project_type', 'created_by', 'updated_by', 'planning', 
                                                        'planning__created_by', 'planning__updated_by').all()
        for project_detail in queryset:
            project_detail.format_timestamp("%d %B %Y")
            project_detail.planning.format_timestamp("%d %B %Y")
            project_detail.planning.format_duedate("%d %B %Y")
        
        serializer = ProjectDetailResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        project_detail = ProjectDetail.objects.select_related('project_type', 'created_by', 'updated_by', 'planning', 
                                                        'planning__created_by', 'planning__updated_by'
                                                    ).get(pk=kwargs['pk'])
        project_detail.format_timestamp("%d %B %Y")
        project_detail.planning.format_timestamp("%d %B %Y")
        project_detail.planning.format_duedate("%d %B %Y")
        serializer = ProjectDetailResponseSerializer(project_detail, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        project_detail = super().create(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.CREATE, TableEnum.PROJECT_DETAIL)
        return project_detail

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        project_detail = super().update(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)
        return project_detail

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']                       
        project_detail = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.DELETE, TableEnum.PROJECT_DETAIL)
        return project_detail
        
    
            