from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models.project_detail_model import ProjectDetail
from api.models.user_model import User
from api.serializers import ProjectDetailSerializer
from api.utils.date_format import timestamp_to_strdateformat
from rest_framework.decorators import action
from copy import deepcopy

from api.models import ProjectDetail
from api.serializers import ProjectDetailSerializer
from api.utils.date_format import timestamp_to_strdateformat

from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum


class ProjectDetailViewSet(viewsets.ModelViewSet):
    queryset = ProjectDetail.objects.all()
    serializer_class = ProjectDetailSerializer

    def list(self, request, *args, **kwargs):
        project_detail = super().list(request, *args, **kwargs)
        for each in project_detail.data:
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return project_detail
    
    def retrieve(self, request, *args, **kwargs):
        project_detail = super().retrieve(request, *args, **kwargs)
        project_detail.data['created_at'] = timestamp_to_strdateformat(project_detail.data['created_at'], "%d %B %Y")
        project_detail.data['updated_at'] = timestamp_to_strdateformat(project_detail.data['updated_at'], "%d %B %Y")
        return project_detail

    def create(self, request, *args, **kwargs):
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
        
    
            