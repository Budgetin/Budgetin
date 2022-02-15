from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Project
from api.permissions import IsAuthenticated, IsUser
from api.serializers import ProjectResponseSerializer

class MyProjectViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsUser]
            
    def list(self, request):
        user_ithc_biro = request.custom_user['ithc_biro']

        queryset = Project.objects.select_related('biro', 'product', 'product__strategy', 'updated_by', 'created_by').all()            
        queryset = queryset.filter(biro__ithc_biro=user_ithc_biro)
        
        for project in queryset:
            project.format_timestamp("%d %B %Y")
            
        serializer = ProjectResponseSerializer(queryset, many=True)
        return Response(serializer.data)