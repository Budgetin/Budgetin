from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Monitoring, Budget
from api.permissions import IsAuthenticated, IsUser
from api.serializers import MonitoringSerializer, BudgetResponseSerializer
from api.utils.enum import MonitoringStatusEnum

from api.utils.export_budget import export_budget_as_excel

class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsUser]
            
    def list(self, request):
        queryset = Monitoring.objects.select_related('planning', 'biro').all()
        queryset = queryset.filter(pic_initial=request.custom_user['initial'])
        
        for monitoring in queryset:
            monitoring.format_timestamp("%d %B %Y")                

        serializer = MonitoringSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        monitoring = Monitoring.objects.get(pk=pk)
        monitoring.format_timestamp("%d %B %Y")

        serializer = MonitoringSerializer(monitoring, many=False)
        return Response(serializer.data)
    
    @action(methods=['get'], detail=False, url_path=r'submitted_budget/(?P<monitoring_id>\d+)')
    def submitted_budget(self, request, monitoring_id):
        monitoring = Monitoring.objects.select_related('planning').get(pk=monitoring_id)
        planning_id = monitoring.planning.id
        user_ithc_biro = request.custom_user['ithc_biro']        
        
        queryset = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'created_by', 'updated_by')
        queryset = queryset.filter(project_detail__planning__id=planning_id)
        queryset = queryset.filter(project_detail__project__biro__ithc_biro=user_ithc_biro)
        
        for budget in queryset:
            budget.format_timestamp("%d %B %Y")
        
        serializer = BudgetResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        monitoring = Monitoring.objects.filter(pk=pk).update(monitoring_status=MonitoringStatusEnum.SUBMITTED.value)
        return Response({"message":"Monitoring "+ str(pk) +" status changed to Submitted"})
        
    @action(detail=False, methods=['get'], url_path=r'submitted_budget/(?P<monitoring_id>\d+)/download')
    def export(self, request, monitoring_id):
        monitoring = Monitoring.objects.select_related('planning').get(pk=monitoring_id)
        planning_id = monitoring.planning.id
        user_ithc_biro = request.custom_user['ithc_biro']        
        
        queryset = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'created_by', 'updated_by')
        queryset = queryset.filter(project_detail__planning__id=planning_id)
        queryset = queryset.filter(project_detail__project__biro__ithc_biro=user_ithc_biro)
        
        return export_budget_as_excel(queryset)
        