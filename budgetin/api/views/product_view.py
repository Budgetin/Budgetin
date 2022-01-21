import json
from rest_framework import viewsets
from api.models import Product,Strategy
from api.serializers.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        strategy = super().list(request, *args, **kwargs)
        for i in strategy.data:
            strategy_id = i['strategy']
            strategy_name = Strategy.objects.filter(id=strategy_id).first().name
            i['strategy'] = {"id":strategy_id,"name":strategy_name}
        return strategy

    def retrieve(self, request, *args, **kwargs):
        strategy = super().retrieve(request, *args, **kwargs)
        strategy_id = strategy.data['strategy']
        strategy_name = Strategy.objects.filter(id=strategy_id).first().name
        strategy.data['strategy'] = {"id":strategy_id,"name":strategy_name}
        return strategy