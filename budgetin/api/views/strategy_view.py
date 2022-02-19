from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.models import Strategy
from api.serializers import StrategySerializer, StrategyResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_excel, read_file
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
        file = read_file(request)
        df = read_excel(file, 'strategy')
        errors = []
        
        for index, data in df.iterrows():
            errors.extend(self.insert_to_db(request, data, (index+2)))
            
        if errors:
            raise ValidationException(errors)

        return Response(status=204)
    
    def insert_to_db(self, request, data, index):
        errors = self.validate_data(data, index)
        
        if not errors:
            strategy = self.create_strategy(request, data)
            AuditLog.Save(StrategySerializer(strategy), request, ActionEnum.CREATE, TableEnum.STRATEGY)

        return errors
            
    def validate_data(self, data, index):
        errors = []
        errors = self.validate_strategy(data, index, errors)
        return errors
    
    def validate_strategy(self, data, index, errors):
        name = data['strategy_name']
        if Strategy.name_exists(name):
            errors.append("Strategy '{}' at line {} already exists".format(name, index))
        return errors
    
    def create_strategy(self, request, data):
        return Strategy.objects.create(
            name = data['strategy_name'],
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )