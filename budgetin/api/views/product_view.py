from rest_framework import viewsets
from api.models import Product,Strategy
from api.serializers.product_serializer import ProductSerializer
from api.utils.date_format import timestamp_to_strdateformat

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
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return product

    def retrieve(self, request, *args, **kwargs):
        #include strategy
        product = super().retrieve(request, *args, **kwargs)
        strategy_id = product.data['strategy']
        strategy_name = Strategy.objects.filter(id=strategy_id).first().name
        product.data['strategy'] = {"id":strategy_id,"name":strategy_name}

        #reformat date
        product.data['created_at'] = timestamp_to_strdateformat(product.data['created_at'], "%d %B %Y")
        product.data['updated_at'] = timestamp_to_strdateformat(product.data['updated_at'], "%d %B %Y")
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