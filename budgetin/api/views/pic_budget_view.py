from rest_framework import viewsets
from api.models.pic_budget_model import PicBudget
from api.serializers.pic_budget_serializer import PicBudgetSerializer

class PicBudgetViewSet(viewsets.ModelViewSet):
    queryset = PicBudget.objects.all()
    serializer_class = PicBudgetSerializer
