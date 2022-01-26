import json
from rest_framework import viewsets
from rest_framework.decorators import action
from api.models import Planning, User
from api.serializers.planning_serializer import PlanningSerializer
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.send_email import send_email
from rest_framework.response import Response
from api.models.monitoring_model import Monitoring
from api.models.biro_model import Biro
from api.models.monitoring_status_model import MonitoringStatus
from api.utils.hit_api import get_all_biro
from api.utils.enum import MonitoringStatusEnum
from api.utils.biro import create_update_all_biro
from django.db import transaction

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class PlanningViewSet(viewsets.ModelViewSet):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer

    def list(self, request, *args, **kwargs):
        planning = super().list(request, *args, **kwargs)
        for each in planning.data:
            each['due_date'] = timestamp_to_strdateformat(each['due_date'], "%d %B %Y")
            if each['updated_by'] is not None:
                each['updated_by'] = User.objects.get(pk=each['updated_by']).display_name
            else:
                each['updated_by'] = ""
            each['created_by'] = User.objects.get(pk=each['created_by']).display_name
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return planning
    
    def retrieve(self, request, *args, **kwargs):
        planning = super().retrieve(request, *args, **kwargs)
        planning.data['due_date'] = timestamp_to_strdateformat(planning.data['due_date'], "%d %B %Y")
        if planning.data['updated_by'] is not None:
            planning.data['updated_by'] = User.objects.get(pk=planning.data['updated_by']).display_name
        else:
            planning.data['updated_by'] = ""
        planning.data['created_by'] = User.objects.get(pk=planning.data['created_by']).display_name
        planning.data['created_at'] = timestamp_to_strdateformat(planning.data['created_at'], "%d %B %Y")
        planning.data['updated_at'] = timestamp_to_strdateformat(planning.data['updated_at'], "%d %B %Y")
        return planning

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        
        #Process send notification
        if 'send_notification' in request.data:
            if request.data['send_notification'] == True:
                if 'biros' and 'body' in request.data:
                    biro_id_list = request.data['biros']
                    subject = "[Budgetin] Akses Input Budget"
                    body = request.data['body']
                    if len(biro_id_list) > 0 and body != "":
                        send_email(biro_id_list, subject, body)
        
        planning = super().create(request, *args, **kwargs)
        AuditLog.Save(planning, request, ActionEnum.CREATE, TableEnum.PLANNING)
        
        biros = get_all_biro()
        for biro in biros:
            monitoring_status_id = MonitoringStatus.objects.filter(name=MonitoringStatusEnum.TODO.value).values()[0]['id']
            Monitoring.objects.create(biro_id=biro['id'], planning_id=planning.data['id'], monitoring_status_id=monitoring_status_id)
        
        #Re-seed biro data
        create_update_all_biro(biros)

        return planning

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1

        #Process send notification
        if 'send_notification' in request.data:
            if request.data['send_notification'] == True:
                if 'biros' and 'body' in request.data:
                    biro_id_list = request.data['biros']
                    subject = "[Budgetin] Akses Input Budget"
                    body = request.data['body']
                    if len(biro_id_list) > 0 and body != "":
                        send_email(biro_id_list, subject, body)
        
        planning = super().update(request, *args, **kwargs)
        AuditLog.Save(planning, request, ActionEnum.UPDATE, TableEnum.PLANNING)
        return planning

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        planning = super().destroy(request, *args, **kwargs)
        AuditLog.Save(planning, request, ActionEnum.DELETE, TableEnum.PLANNING)
        return planning
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_planning = Planning.objects.filter(is_active=True).values()
        
        return Response(active_planning)