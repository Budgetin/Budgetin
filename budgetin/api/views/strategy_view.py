from rest_framework import viewsets 
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.models import Strategy
from api.serializers import StrategySerializer, StrategyResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_file, get_import_template_path, load_file
from api.utils.excel import read_excel, export_excel
from api.exceptions import ValidationException

def is_duplicate_create(name):
    if Strategy.objects.filter(name__iexact=name):
        raise ValidationException('Strategy ' + name + ' already exists')

def is_duplicate(id, name):
    if Strategy.objects.filter(name__iexact=name).exclude(pk=id):
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
        request.data['name'] = request.data['name'].split()
        is_duplicate_create(request.data['name'])
        strategy = super().create(request, *args, **kwargs)
        AuditLog.Save(strategy, request, ActionEnum.CREATE, TableEnum.STRATEGY)
        return strategy

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['name'] = request.data['name'].split()
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
        df = read_excel(file, TableEnum.STRATEGY.value)
        
        for index, data in df.iterrows():
            strategy_name = data['strategy_name']

            if not Strategy.name_exists(strategy_name):
                self.insert_to_db(request, data)

        return Response(status=204)
    
    def insert_to_db(self, request, data):
        strategy = self.create_strategy(request, data['strategy_name'])
        AuditLog.Save(StrategySerializer(strategy), request, ActionEnum.CREATE, TableEnum.STRATEGY)
            
    def create_strategy(self, request, strategy_name):
        return Strategy.objects.create(
            name=strategy_name,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )
        
    @action(methods=['get'], detail=False, url_path='import/template')
    def download_import_template(self, request):
        file_path = get_import_template_path(TableEnum.STRATEGY)
        file = load_file(file_path, 'rb')
        
        return export_excel(file, 'import_template_strategy.xlsx')