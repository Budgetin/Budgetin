from rest_framework.response import Response

from api.models import Strategy
from api.serializers import StrategySerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_file
from api.utils.excel import read_excel

class ImportStrategy():
    def start(self, request):
        file = read_file(request)
        df = read_excel(file, TableEnum.STRATEGY.value)

        # create empty strategy
        Strategy.objects.get_or_create(name='None')
        
        # Fetch all strategies and convert it to Key, Value dictionary
        strategies = dict((strategy.name.lower(), strategy) for strategy in Strategy.objects.all())
        
        for _, data in df.iterrows():
            strategy_name = data['strategy_name'].strip()
            
            if strategy_name.lower() not in strategies:
                strategy = self.create_strategy(request, strategy_name)
                strategies[strategy_name.lower()] = strategy

        return Response(status=204)
    
    def create_strategy(self, request, strategy_name):
        strategy = Strategy.objects.create(
            name=strategy_name,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )
        AuditLog.Save(StrategySerializer(strategy), request, ActionEnum.CREATE, TableEnum.STRATEGY)
        return strategy