from rest_framework import viewsets
from api.models.planning_model import Planning
from api.serializers.planning_serializer import PlanningSerializer
from api.utils.date_format import timestamp_to_strdateformat

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class PlanningViewSet(viewsets.ModelViewSet):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer

    def list(self, request, *args, **kwargs):
        planning = super().list(request, *args, **kwargs)
        for each in planning.data:
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return planning
    
    def retrieve(self, request, *args, **kwargs):
        planning = super().retrieve(request, *args, **kwargs)
        planning.data['created_at'] = timestamp_to_strdateformat(planning.data['created_at'], "%d %B %Y")
        planning.data['updated_at'] = timestamp_to_strdateformat(planning.data['updated_at'], "%d %B %Y")
        return planning

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        planning = super().create(request, *args, **kwargs)
        AuditLog.Save(planning, request, ActionEnum.CREATE, TableEnum.PLANNING)
        return planning

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        planning = super().update(request, *args, **kwargs)
        AuditLog.Save(planning, request, ActionEnum.UPDATE, TableEnum.PLANNING)
        return planning

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        planning = super().destroy(request, *args, **kwargs)
        AuditLog.Save(planning, request, ActionEnum.DELETE, TableEnum.PLANNING)
        return planning