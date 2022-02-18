from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.models import Strategy
from api.serializers import StrategySerializer, StrategyResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_excel
from api.exceptions import ValidationException

def is_duplicate_create(name):
    if Strategy.objects.filter(name=name):
        raise ValidationException('Strategy ' + name + ' already exists')

def is_duplicate(id, name):
    if Strategy.objects.filter(name=name).exclude(pk=id):
        raise ValidationException('Strategy ' + name + ' already exists')

class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    
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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        is_duplicate_create(request.data['name'])
        strategy = super().create(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.CREATE, TableEnum.STRATEGY)
        return strategy

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        is_duplicate(kwargs['pk'], request.data['name'])
        strategy = super().update(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.UPDATE, TableEnum.STRATEGY)
        return strategy

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        strategy = super().destroy(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.DELETE, TableEnum.STRATEGY)
        return strategy
    
    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='import')
    def import_from_excel(self, request):
        file = request.FILES['file'].read()
        df = read_excel(file, 'strategy')
        
        for index, row in df.iterrows():
            self.insert_to_db(request, row, (index+2))
        
        return Response(status=204)
    
    def insert_to_db(self, request, data, index):
        name = data['strategy_name']
        if self.strategy_already_exists(name):
            raise ValidationException('Strategy {} at line {} already exists'.format(name, index))

        strategy = self.create_strategy(request, name)
        AuditLog.Save(StrategySerializer(strategy), request, ActionEnum.UPDATE, TableEnum.STRATEGY) 
            
    def strategy_already_exists(self, name):
        return Strategy.objects.filter(name=name).count() > 0
    
    def create_strategy(self, request, name):
        return Strategy.objects.create(
            name = name,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )