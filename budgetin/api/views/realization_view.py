from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Realization
from api.serializers import RealizationSerializer, RealizationResponseSerializer
from api.views.upload.import_realisasi import ImportRealisasi
from api.utils import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.permissions import IsAuthenticated, IsAdminOrReadOnly

class RealizationViewSet(viewsets.ModelViewSet):
    queryset = Realization.objects.all()
    serializer_class = RealizationSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
    def list(self, request, *args, **kwargs):
        queryset = Realization.objects.all()

        serializer = RealizationResponseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Realization.objects.get(pk=kwargs['pk'])
        
        serializer = RealizationResponseSerializer(queryset, many=False)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        realization = super().update(request, *args, **kwargs) 
        AuditLog.Save(realization, request, ActionEnum.UPDATE.value, TableEnum.REALIZATION.value)
        return realization
    
    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        realization = super().create(request, *args, **kwargs)
        AuditLog.Save(realization, request, ActionEnum.CREATE.value, TableEnum.REALIZATION.value)
        return realization
    
    @action(methods=['post'], detail=False, url_path='import')
    def import_realisasi(self, request):
        ImportRealisasi().start(request)
