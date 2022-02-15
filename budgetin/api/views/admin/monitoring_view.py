from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from api.utils.hit_api import get_all_biro
from api.views.admin.planning_view import create_update_biro, create_monitoring

from api.models import Monitoring
from api.serializers import MonitoringSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum, MonitoringStatusEnum
from api.permissions import IsAuthenticated, IsAdmin
from api.exceptions.not_found_exception import NotFoundException

def create_non_existent_biro(biros, planning_id):
    for ithc_biro in biros:
        biro, created = create_update_biro(ithc_biro)
        # Biro that lasts with * (IBO*, NIS*) is not included
        if created and ithc_biro["code"][-1] != "*":
            create_monitoring(ithc_biro, biro, planning_id)
            
class MonitoringViewSet(viewsets.ModelViewSet):
    queryset = Monitoring.objects.all()
    serializer_class = MonitoringSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def list(self, request, *args, **kwargs):
        planning  = request.GET.get('planning')
        if planning:
            queryset = Monitoring.objects.select_related('biro', 'planning').filter(planning=planning)
        else:
            queryset = Monitoring.objects.select_related('biro', 'planning').all()

        queryset.filter(~Q(monitoring_status=MonitoringStatusEnum.OPTIONAL.value))
        for monitoring in queryset:
            monitoring.format_timestamp("%d %B %Y")

        serializer = MonitoringSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        id = kwargs['pk']
        monitoring = Monitoring.objects.select_related('biro', 'planning').get(pk=id)
        
        serializer = MonitoringSerializer(monitoring, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        monitoring = super().create(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, ActionEnum.CREATE, TableEnum.MONITORING)
        return monitoring

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        monitoring = super().update(request, *args, **kwargs)
        AuditLog.Save(monitoring, request, ActionEnum.UPDATE, TableEnum.MONITORING)
        return monitoring

    def destroy(self, request, *args, **kwargs):
        return Response({
            'message': 'Monitoring cannot be deleted'
        })

    @action(detail=False, methods=['get'])
    def reload(self, request):
        try:
            planning_id = request.query_params.getlist('planning')[0]
        except KeyError:
            raise NotFoundException("Planning parameter")

        biros = get_all_biro('manager_employee,sub_group,sub_group.group,manager_employee,sub_group.manager_employee,sub_group.group.manager_employee')
        create_non_existent_biro(biros, planning_id)
        return Response({"message":"Biro for planning "+ str(planning_id) +" Reloaded"})

    @action(detail=True, methods=['get'])
    def submit(self, request, pk=None):
        monitoring = Monitoring.objects.filter(pk=pk).update(monitoring_status="Submitted")
        return Response({"message":"Monitoring "+ str(pk) +"status changed to : Submitted"})