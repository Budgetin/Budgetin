from rest_framework import viewsets 
from rest_framework.response import Response

from api.permissions import IsAuthenticated, IsAdmin
from api.models import Strategy
from api.serializers import StrategySerializer, StrategyResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.auditlog import AuditLog
from api.exceptions.validation_exception import ValidationException

def is_duplicate_create(name):
    if Strategy.objects.filter(name=name):
        raise ValidationException

def is_duplicate(id, name):
    if Strategy.objects.filter(name=name).exclude(pk=id):
        raise ValidationException

class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = Strategy.objects.select_related('updated_by','created_by').all()
        for strategy in queryset:
            strategy.format_timestamp("%d %B %Y")
        
        serializer = StrategyResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        strategy = Strategy.objects.select_related('updated_by','created_by').get(pk=kwargs['pk'])
        strategy.format_timestamp("%d %B %Y")
        
        serializer = StrategyResponseSerializer(strategy, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        is_duplicate_create(request.data['name'])
        strategy = super().create(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.CREATE, TableEnum.STRATEGY)
        return strategy

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        is_duplicate(kwargs['pk'], request.data['name'])
        strategy = super().update(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.UPDATE, TableEnum.STRATEGY)
        return strategy

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        strategy = super().destroy(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.DELETE, TableEnum.STRATEGY)
        return strategy