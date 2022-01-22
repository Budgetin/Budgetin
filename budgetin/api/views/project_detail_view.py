from rest_framework import viewsets
from api.models.project_detail_model import ProjectDetail
from api.serializers.project_detail_serializer import ProjectDetailSerializer
from datetime import datetime

#For Audit Logging
from api.utils.auditlog import AuditLog

class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer

    def list(self, request, *args, **kwargs):
        project_detail = super().list(request, *args, **kwargs)
        for each in project_detail.data:
            createdDate = each['created_at']
            date_time_obj = datetime.fromisoformat(createdDate)
            each['created_at'] = date_time_obj.strftime("%d %B %Y")

            updatedDate = each['updated_at']
            date_time_obj = datetime.fromisoformat(updatedDate)
            each['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return project_detail
    
    def retrieve(self, request, *args, **kwargs):
        project_detail = super().retrieve(request, *args, **kwargs)
        createdDate = project_detail.data['created_at']
        date_time_obj = datetime.fromisoformat(createdDate)
        project_detail.data['created_at'] = date_time_obj.strftime("%d %B %Y")

        updatedDate = project_detail.data['updated_at']
        date_time_obj = datetime.fromisoformat(updatedDate)
        project_detail.data['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return project_detail

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        project_detail = super().create(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, AuditLog.Create, AuditLog.ProjectDetail)
        return project_detail

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        project_detail = super().update(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, AuditLog.Update, AuditLog.ProjectDetail)
        return project_detail

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        project_detail = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, AuditLog.Delete, AuditLog.ProjectDetail)
        return project_detail