from rest_framework import viewsets
from api.models.project_detail_model import ProjectDetail
from api.serializers.project_detail_serializer import ProjectDetailSerializer
from api.utils.date_format import timestamp_to_dateformat

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer

    def list(self, request, *args, **kwargs):
        project_detail = super().list(request, *args, **kwargs)
        for each in project_detail.data:
            each['created_at'] = timestamp_to_dateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_dateformat(each['updated_at'], "%d %B %Y")
        return project_detail
    
    def retrieve(self, request, *args, **kwargs):
        project_detail = super().retrieve(request, *args, **kwargs)
        project_detail.data['created_at'] = timestamp_to_dateformat(project_detail.data['created_at'], "%d %B %Y")
        project_detail.data['updated_at'] = timestamp_to_dateformat(project_detail.data['updated_at'], "%d %B %Y")
        return project_detail

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        project_detail = super().create(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.CREATE, TableEnum.PROJECT_DETAIL)
        return project_detail

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        project_detail = super().update(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)
        return project_detail

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        project_detail = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.DELETE, TableEnum.PROJECT_DETAIL)
        return project_detail