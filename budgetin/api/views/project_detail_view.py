from django.forms import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models.project_detail_model import ProjectDetail
from api.models.user_model import User
from api.serializers.project_detail_serializer import ProjectDetailSerializer
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
        if kwargs.get('pk') is not None:
            projectdetails = ProjectDetail.objects.select_related('planning', 'project', 'project_type', 'project__biro', 'project__product').filter(id=kwargs.get('pk'))
        else:
            projectdetails = ProjectDetail.objects.select_related('planning', 'project', 'project_type', 'project__biro', 'project__product').all()
            
        result = []
        counter = 1
        for projectdetail in projectdetails:
            dict = model_to_dict(projectdetail)
            dict['created_by'] = User.objects.get(pk=projectdetail.created_by).display_name
            dict['project_detail_id'] = projectdetail.id
            dict['planning'] = model_to_dict(projectdetail.planning)
            dict['project'] = model_to_dict(projectdetail.project)
            dict['project_type'] = projectdetail.project_type.name
            dict['project']['product'] = model_to_dict(projectdetail.project.product)
            dict['project']['product']['strategy'] = model_to_dict(projectdetail.project.product.strategy)
            dict['project']['biro'] = projectdetail.project.biro.code
            dict['created_at'] = projectdetail.created_at.strftime("%d %B %Y")
            dict['updated_at'] = projectdetail.updated_at.strftime("%d %B %Y")
            
            curr_budgets = projectdetail.budget.select_related('coa').all()
            
            if len(curr_budgets) > 0:
                for budget in curr_budgets:
                    new_dict = deepcopy(dict)
                    new_dict['project']['budget'] = model_to_dict(budget)
                    new_dict['project']['budget']['planning_nominal'] = budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4
                    new_dict['project']['budget']['coa'] = model_to_dict(budget.coa)
                    new_dict['id'] = counter
                    result.append(new_dict)
                    counter = counter+1
            else:
                dict['project']['budget'] = None
                dict['id'] = counter
                result.append(dict)
                counter = counter+1
                
        if kwargs.get('pk') is not None:
            return Response(result[0])
        else:
            return Response(result)
    
            