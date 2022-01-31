from rest_framework import viewsets 
from rest_framework.response import Response

from api.models import Strategy, User
from api.serializers import StrategySerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.auditlog import AuditLog
from api.exceptions.validation_exception import ValidationException

def is_duplicate(name):
    if Strategy.objects.filter(name=name):
        raise ValidationException
class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer

    
    def list(self, request, *args, **kwargs):
        queryset = Strategy.objects.all()
        for strategy in queryset:
            strategy.format_timestamp("%d %B %Y")
            strategy.format_created_updated_by()
        
        serializer = StrategySerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        strategy = Strategy.objects.get(pk=kwargs['pk'])
        strategy.format_timestamp("%d %B %Y")
        strategy.format_created_updated_by()
        
        serializer = StrategySerializer(strategy, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        is_duplicate(request.data['name'])
        strategy = super().create(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.CREATE, TableEnum.STRATEGY)
        return strategy

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        is_duplicate(request.data['name'])
        strategy = super().update(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.UPDATE, TableEnum.STRATEGY)
        return strategy

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        strategy = super().destroy(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.DELETE, TableEnum.STRATEGY)
        return strategy