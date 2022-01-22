from datetime import datetime
from rest_framework import viewsets
from api.models import Product,Strategy
from api.serializers.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        strategy = super().list(request, *args, **kwargs)
        for each in strategy.data:
            #include strategy
            strategy_id = each['strategy']
            strategy_name = Strategy.objects.filter(id=strategy_id).first().name
            each['strategy'] = {"id":strategy_id,"name":strategy_name}
            #Reformat date
            createdDate = each['created_at']
            date_time_obj = datetime.fromisoformat(createdDate)
            each['created_at'] = date_time_obj.strftime("%d %B %Y")
        return strategy

    def retrieve(self, request, *args, **kwargs):
        #include strategy
        strategy = super().retrieve(request, *args, **kwargs)
        strategy_id = strategy.data['strategy']
        strategy_name = Strategy.objects.filter(id=strategy_id).first().name
        strategy.data['strategy'] = {"id":strategy_id,"name":strategy_name}

        #reformat date
        createdDate = strategy.data['created_at']
        date_time_obj = datetime.fromisoformat(createdDate)
        strategy.data['created_at'] = date_time_obj.strftime("%d %B %Y")
        return strategy