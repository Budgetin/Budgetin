from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Project
from api.serializers import ProjectSerializer, ProjectResponseSerializer, ProjectResponseDetailSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.permissions import IsAuthenticated, IsAdmin

def get_filtered_queryset(request, queryset):
    planning = request.query_params.get('planning')
    if planning:
        queryset = queryset.filter(project_detail__planning=planning)
        
    return queryset

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.select_related('biro', 'product', 'product__strategy', 'updated_by', 'created_by').all()            
        queryset = get_filtered_queryset(request, queryset)
            
        for project in queryset:
            project.format_timestamp("%d %B %Y")
        serializer = ProjectResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        project = Project.objects.select_related('biro', 'product', 'product__strategy', 'updated_by', 'created_by').prefetch_related(
                'project_detail', 'project_detail__planning', 'project_detail__project', 'project_detail__project_type'
            ).get(pk=kwargs['pk'])
        project.format_timestamp("%d %B %Y")
            
        serializer = ProjectResponseDetailSerializer(project, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        project = super().create(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.CREATE, TableEnum.PROJECT)
        return project

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        project = super().update(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.UPDATE, TableEnum.PROJECT)
        return project

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']                       
        project = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.DELETE, TableEnum.PROJECT)
        return project

    def list_for_export():
        queryset = Project.objects.all()
        for project in queryset:
            project.format_timestamp("%d %B %Y")
            
        serializer = ProjectResponseSerializer(queryset, many=True)
        return Response(serializer.data)