from rest_framework import viewsets
from api.models import Product,Strategy
from api.serializers.product_serializer import ProductSerializer
from datetime import datetime

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

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

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        product = super().create(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.CREATE, TableEnum.PRODUCT)
        return product

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        product = super().update(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.UPDATE, TableEnum.PRODUCT)
        return product

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        product = super().destroy(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.DELETE, TableEnum.PRODUCT)
        return product