from rest_framework import viewsets
from budgetin.api.serializers.budget_serializer import BudgetSerializer 
from models.budget_model import Budget
from serializers.budget_serializer import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer