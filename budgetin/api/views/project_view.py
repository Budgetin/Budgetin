from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Project
from api.serializers import ProjectSerializer, ProjectResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        queryset = Project.objects.all()
        for project in queryset:
            project.format_timestamp("%d %B %Y")
            
        serializer = ProjectResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        project = Project.objects.get(pk=kwargs['pk'])
        project.format_timestamp("%d %B %Y")
            
        serializer = ProjectResponseSerializer(project, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        project = super().create(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.CREATE, TableEnum.PROJECT)
        return project

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        project = super().update(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.UPDATE, TableEnum.PROJECT)
        return project

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1                                 
        project = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.DELETE, TableEnum.PROJECT)
        return project

    def list_for_export():
        queryset = Project.objects.all()
        for project in queryset:
            project.format_timestamp("%d %B %Y")
            
        serializer = ProjectResponseSerializer(queryset, many=True)
        return Response(serializer.data)