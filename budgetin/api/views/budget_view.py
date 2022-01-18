from rest_framework import viewsets 
from models.budget_model import Budget
from serializers.strategy_serializer import StrategySerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = StrategySerializer