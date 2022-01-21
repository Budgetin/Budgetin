from venv import create
from rest_framework import viewsets
from api.models.budget_model import Budget
from api.serializers.budget_serializer import BudgetSerializer

class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    