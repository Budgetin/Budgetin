from rest_framework import viewsets
from api.models.project_model import Project
from api.serializers.project_serializer import ProjectSerializer
from api.utils.date_format import timestamp_to_dateformat

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        project = super().list(request, *args, **kwargs)
        for each in project.data:
            each['created_at'] = timestamp_to_dateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_dateformat(each['updated_at'], "%d %B %Y")
        return project
    
    def retrieve(self, request, *args, **kwargs):
        project = super().retrieve(request, *args, **kwargs)
        project.data['created_at'] = timestamp_to_dateformat(project.data['created_at'], "%d %B %Y")
        project.data['updated_at'] = timestamp_to_dateformat(project.data['updated_at'], "%d %B %Y")
        return project

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        project = super().create(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.CREATE, TableEnum.PROJECT)
        return project

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        project = super().update(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.UPDATE, TableEnum.PROJECT)
        return project

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        project = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project, request, ActionEnum.DELETE, TableEnum.PROJECT)
        return project