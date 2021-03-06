from django.db import transaction
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db import transaction

from api.models import Planning, Monitoring, Biro
from api.serializers import PlanningSerializer, PlanningResponseSerializer, ActivePlanningSerializer
from api.utils.send_email import send_email
from api.utils.hit_api import get_all_biro
from api.utils.enum import MonitoringStatusEnum
from api.utils.manager_email import get_managers_email_list
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.permissions import IsAuthenticated, IsAdminOrReadOnly

@transaction.atomic
def create_update_all_biro_and_create_monitoring(biros, planning_id):
    for ithc_biro in biros:
        biro, created = create_update_biro(ithc_biro)

        # Biro that lasts with * (IBO*, NIS*) is not included
        if ithc_biro["code"][-1] != "*":
            create_monitoring(ithc_biro, biro, planning_id, MonitoringStatusEnum.TODO.value)
        else:
            create_monitoring(ithc_biro, biro, planning_id, MonitoringStatusEnum.OPTIONAL.value)

@transaction.atomic
def create_update_biro(biro):
    return Biro.objects.update_or_create(
        ithc_biro=biro['id'],
        defaults={'code': biro['code'], 
                    'name': biro['name'],
                    'sub_group_code': biro['sub_group']['code'],
                    'group_code': biro['sub_group']['group']['code'],
                    'rcc': biro['sub_group']['rcc'],
                    }
        )
        
@transaction.atomic
def create_monitoring(ithc_biro, biro, planning_id, monitoring_status):
    pic = get_pic(ithc_biro)
    
    Monitoring.objects.create(
        biro_id=biro.id, 
        planning_id=planning_id, 
        monitoring_status=monitoring_status,
        pic_employee_id=pic['id'] if pic else None, #DEBT. Delete if else when Biro* already has manager
        pic_initial=pic['initial'] if pic else None, #DEBT. Delete if else when Biro* already has manager
        pic_display_name=pic['display_name'] if pic else None, #DEBT. Delete if else when Biro* already has manager
    )
    
def get_pic(ithc_biro):
    if ithc_biro["manager_employee"] is not None:
        return ithc_biro["manager_employee"]
    if ithc_biro["sub_group"]["manager_employee"] is not None:
        return ithc_biro["sub_group"]["manager_employee"]

    return ithc_biro["sub_group"]["group"]["manager_employee"]
    
def is_send_notification(request):
    field_exists = 'notification' and 'biros' and 'body' in request.data 
    if not field_exists:
        return False
    
    field_valid = request.data['notification'] == True and request.data['body'] != '' and len(request.data['biros']) > 0
    return field_valid
    
def send_notification(request, biros=''):
    biro_id_list = request.data['biros']
    subject = "[noreply] budgetin"
    body = request.data['body']
    receiver_email_list = get_receiver_email_list(biros, biro_id_list)
    
    send_email(subject, body, receiver_email_list)
    return receiver_email_list
        
def get_receiver_email_list(biros, biro_id_list):
    receiver_email_list = get_managers_email_list(biro_id_list, biros)

    # remove duplicate email
    receiver_email_list = list(dict.fromkeys(receiver_email_list))
    
    return receiver_email_list

def get_biros_code(biros_id):
    biros = Biro.objects.filter(ithc_biro__in=biros_id)
    biros_code = []
    for biro in biros:
        biros_code.append(biro.code)

    return biros_code

class PlanningViewSet(viewsets.ModelViewSet):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Planning.objects.select_related('updated_by', 'created_by').all()
        for planning in queryset:
            planning.format_duedate("%Y-%m-%d")
            planning.format_timestamp("%d %B %Y")

        serializer = PlanningResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        planning = Planning.objects.select_related('updated_by', 'created_by').get(pk=kwargs['pk'])
        planning.format_duedate("%Y-%m-%d")
        planning.format_timestamp("%d %B %Y")
        
        serializer = PlanningResponseSerializer(planning, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        planning = super().create(request, *args, **kwargs)
        
        planning_id = planning.data['id']
        biros = get_all_biro('manager_employee,sub_group,sub_group.group,manager_employee,sub_group.manager_employee,sub_group.group.manager_employee')
        create_update_all_biro_and_create_monitoring(biros, planning_id)
        
        #Process send notification
        if is_send_notification(request):
            # send_notification(request, biros) #DEBT. Uncomment this line
            planning.data['body'] = request.data['body']
            planning.data['send_to'] = get_biros_code(request.data['biros'])
            
        AuditLog.Save(planning, request, ActionEnum.CREATE, TableEnum.PLANNING)
        
        return planning

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        planning = super().update(request, *args, **kwargs)

        if(is_send_notification(request)):
            # send_notification(request) #DEBT. Uncomment this line
            planning.data['email_body'] = request.data['body']
            planning.data['send_to'] = get_biros_code(request.data['biros'])
        
        AuditLog.Save(planning, request, ActionEnum.UPDATE, TableEnum.PLANNING)
        return planning

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        planning = super().destroy(request, *args, **kwargs)
        AuditLog.Save(planning, request, ActionEnum.DELETE, TableEnum.PLANNING)
        return planning
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        active_planning = Planning.objects.filter(is_active=True).values()
        
        serializer = ActivePlanningSerializer(active_planning, many=True)
        return Response(serializer.data)