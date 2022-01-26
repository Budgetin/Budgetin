from rest_framework import viewsets 
from api.models.strategy_model import Strategy
from api.serializers.strategy_serializer import StrategySerializer
from api.utils.date_format import timestamp_to_strdateformat
from api.models import User
from api.utils.enum import ActionEnum, TableEnum
from api.utils.auditlog import AuditLog
class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    
    def list(self, request, *args, **kwargs):
        strategies = super().list(request, *args, **kwargs)
        for strategy in strategies.data:
            if strategy['updated_by'] is not None:
                strategy['updated_by'] = User.all_objects.get(pk=strategy['updated_by']).display_name
            else:
                strategy['updated_by'] = ''
            strategy['created_by'] = User.all_objects.get(pk=strategy['created_by']).display_name
            strategy['created_at'] = timestamp_to_strdateformat(strategy['created_at'], "%d %B %Y")
            strategy['updated_at'] = timestamp_to_strdateformat(strategy['updated_at'], "%d %B %Y")
        return strategies
    
    def retrieve(self, request, *args, **kwargs):
        strategy = super().retrieve(request, *args, **kwargs)
        if strategy.data['updated_by'] is not None:
                strategy.data['updated_by'] = User.all_objects.get(pk=strategy.data['updated_by']).display_name
        else:
            strategy.data['updated_by'] = ''
        strategy.data['created_by'] = User.all_objects.get(pk=strategy.data['created_by']).display_name
        strategy.data['created_at'] = timestamp_to_strdateformat(strategy.data['created_at'], "%d %B %Y")
        strategy.data['updated_at'] = timestamp_to_strdateformat(strategy.data['updated_at'], "%d %B %Y")
        
        return strategy

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        strategy = super().create(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.CREATE, TableEnum.COA)
        return strategy

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        strategy = super().update(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.UPDATE, TableEnum.COA)
        return strategy

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        strategy = super().destroy(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.DELETE, TableEnum.COA)
        return strategy