from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.models import Monitoring
from api.permissions import IsAuthenticated, IsUser
from api.serializers import MonitoringSerializer

class TaskViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsUser]
            
    def list(self, request):
        queryset = Monitoring.objects.select_related('planning', 'biro').all()
        queryset = queryset.filter(pic_initial=request.custom_user['initial'])
        
        for monitoring in queryset:
            monitoring.format_timestamp("%d %B %Y")                

        serializer = MonitoringSerializer(queryset, many=True)
        return Response(serializer.data)
        
        
        
        