from rest_framework import viewsets 
from api.models.strategy_model import Strategy
from api.serializers.strategy_serializer import StrategySerializer

class StrategyViewSet(viewsets.ModelViewSet):
    queryset = Strategy.objects.all()
    serializer_class = StrategySerializer
