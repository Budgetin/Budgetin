from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models.project_detail_model import ProjectDetail
from api.models.user_model import User
from api.serializers import ProjectDetailSerializer, ProjectDetailResponseSerializer, BudgetResponseSerializer
from api.utils.date_format import timestamp_to_strdateformat
from rest_framework.decorators import action
from copy import deepcopy

from api.models import ProjectDetail
from api.serializers import ProjectDetailSerializer
from api.utils.date_format import timestamp_to_strdateformat

from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

def construct_project_detail(projectdetails):
    result = []
    for projectdetail in projectdetails:
        projectdetail['project_detail_id'] = projectdetail['id']
        projectdetail['id'] = len(result)+1
        
        if len(projectdetail["budget"]) > 0:
            for budget in projectdetail["budget"]:
                new_data = deepcopy(projectdetail)
                new_data['budget'] = budget
                new_data['planning_nominal'] = budget['planning_q1'] + budget['planning_q2'] + budget['planning_q3'] + budget['planning_q4']
                new_data['id'] = len(result)+1
                result.append(new_data)
        else:
            projectdetail['budget'] = None
            result.append(projectdetail)
            
    if len(result) == 1:
        return result[0]
    return result

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
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        project_detail = super().create(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.CREATE, TableEnum.PROJECT_DETAIL)
        return project_detail

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        project_detail = super().update(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)
        return project_detail

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1                                 
        project_detail = super().destroy(request, *args, **kwargs)
        AuditLog.Save(project_detail, request, ActionEnum.DELETE, TableEnum.PROJECT_DETAIL)
        return project_detail
        
    @action(detail=False, methods=['get'])
    def list_planning(self, request, *args, **kwargs):
        projectdetails = ProjectDetail.objects.select_related('planning', 'project', 'project_type', 'project__biro', 'project__product').all()
        
        if 'pk' in kwargs:        
            projectdetails = projectdetails.filter(id=kwargs['pk'])
        
        for projectdetail in projectdetails:
            projectdetail.format_timestamp("%d %B %Y")
            projectdetail.format_created_updated_by()
            projectdetail.project_type_name = projectdetail.project_type.name
        
        serializer = ProjectDetailResponseSerializer(projectdetails, many=True)
        result = construct_project_detail(serializer.data)
        
        return Response(result)


    def list_planning_data(pk=None):
        if pk:        
            projectdetails = ProjectDetail.objects.select_related('planning', 'project', 'project_type', 'project__biro', 'project__product').filter(id=pk)
        else:
            projectdetails = ProjectDetail.objects.select_related('planning', 'project', 'project_type', 'project__biro', 'project__product').all()
        
        for projectdetail in projectdetails:
            projectdetail.format_timestamp("%d %B %Y")
            projectdetail.format_created_updated_by()
            projectdetail.project_type_name = projectdetail.project_type.name
        
        serializer = ProjectDetailResponseSerializer(projectdetails, many=True)
        result = construct_project_detail(serializer.data)
        
        return Response(result)
    
            