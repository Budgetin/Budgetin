from rest_framework import viewsets
from api.models.project_model import Project
from api.serializers.project_serializer import ProjectSerializer
from datetime import datetime

#For Audit Logging
from api.utils.auditlog import AuditLog

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        project = super().list(request, *args, **kwargs)
        for each in project.data:
            createdDate = each['created_at']
            date_time_obj = datetime.fromisoformat(createdDate)
            each['created_at'] = date_time_obj.strftime("%d %B %Y")

            updatedDate = each['updated_at']
            date_time_obj = datetime.fromisoformat(updatedDate)
            each['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return project
    
    def retrieve(self, request, *args, **kwargs):
        project = super().retrieve(request, *args, **kwargs)
        createdDate = project.data['created_at']
        date_time_obj = datetime.fromisoformat(createdDate)
        project.data['created_at'] = date_time_obj.strftime("%d %B %Y")

        updatedDate = project.data['updated_at']
        date_time_obj = datetime.fromisoformat(updatedDate)
        project.data['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return project

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        project = super().create(request, *args, **kwargs)
        AuditLog.Save(project, request, AuditLog.Create, AuditLog.Project)
        return project

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        project = super().update(request, *args, **kwargs)
        AuditLog.Save(project, request, AuditLog.Update, AuditLog.Project)
        return project

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        project = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project, request, AuditLog.Delete, AuditLog.Project)
        return project