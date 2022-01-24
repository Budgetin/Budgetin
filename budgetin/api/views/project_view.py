from rest_framework import viewsets
from api.models.project_model import Project
from api.serializers.project_serializer import ProjectSerializer
from api.utils.date_format import timestamp_to_strdateformat

#For Include
from api.utils.include import include

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def list(self, request, *args, **kwargs):
        project = super().list(request, *args, **kwargs)
        for each in project.data:
            #include strategy
            if request.query_params:
                params = request.query_params.getlist('include')[0].split(",")
                for param in params:
                    paramSplitted = param.split(".")[0]
                    param_name = paramSplitted.lower()
                    paramid = each[param_name]
                    included_data = include(param, paramid)
                    each[param_name] = included_data
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return project
    
    def retrieve(self, request, *args, **kwargs):
        project = super().retrieve(request, *args, **kwargs)
        #include strategy
        if request.query_params:
            params = request.query_params.getlist('include')[0].split(",")
            for param in params:
                paramSplitted = param.split(".")[0]
                param_name = paramSplitted.lower()
                paramid = project.data[param_name]
                included_data = include(param, paramid)
                project.data[param_name] = included_data
        project.data['created_at'] = timestamp_to_strdateformat(project.data['created_at'], "%d %B %Y")
        project.data['updated_at'] = timestamp_to_strdateformat(project.data['updated_at'], "%d %B %Y")
        return project

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