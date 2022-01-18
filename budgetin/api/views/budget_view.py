from rest_framework import viewsets
from models.budget_model import Budget
from serializers.budget_serializer import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer