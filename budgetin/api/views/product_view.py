from datetime import datetime
from rest_framework import viewsets
from api.models import Product,Strategy
from api.serializers.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        product = super().list(request, *args, **kwargs)
        for each in product.data:
            #include strategy
            strategy_id = each['strategy']
            strategy_name = Strategy.objects.filter(id=strategy_id).first().name
            each['strategy'] = {"id":strategy_id,"name":strategy_name}
            #Reformat date
            createdDate = each['created_at']
            date_time_obj = datetime.fromisoformat(createdDate)
            each['created_at'] = date_time_obj.strftime("%d %B %Y")

            updatedDate = each['updated_at']
            date_time_obj = datetime.fromisoformat(updatedDate)
            each['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return product

    def retrieve(self, request, *args, **kwargs):
        #include strategy
        product = super().retrieve(request, *args, **kwargs)
        strategy_id = product.data['strategy']
        strategy_name = Strategy.objects.filter(id=strategy_id).first().name
        product.data['strategy'] = {"id":strategy_id,"name":strategy_name}

        #reformat date
        createdDate = product.data['created_at']
        date_time_obj = datetime.fromisoformat(createdDate)
        product.data['created_at'] = date_time_obj.strftime("%d %B %Y")

        updatedDate = product.data['updated_at']
        date_time_obj = datetime.fromisoformat(updatedDate)
        product.data['updated_at'] = date_time_obj.strftime("%d %B %Y")
        return product