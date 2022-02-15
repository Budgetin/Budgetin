from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Monitoring, Budget
from api.permissions import IsAuthenticated, IsUser
from api.serializers import MonitoringSerializer, BudgetResponseSerializer

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
        monitoring = Monitoring.objects.select_related('planning').get(pk=pk)
        planning_id = monitoring.planning.id
        print(planning_id)
        queryset = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'created_by', 'updated_by')
        queryset = queryset.filter(project_detail__planning__id=planning_id)
        
        serializer = BudgetResponseSerializer(queryset, many=True)
        return Response(serializer.data)
        
        
        
        