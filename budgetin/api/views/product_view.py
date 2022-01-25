from rest_framework import viewsets
from api.models import Product,Strategy,User
from api.serializers.product_serializer import ProductSerializer
from api.utils.date_format import timestamp_to_strdateformat

#For Include
from api.utils.include import include

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def list(self, request, *args, **kwargs):
        product = super().list(request, *args, **kwargs)
        for each in product.data:
            if each['updated_by'] is not None:
                each['updated_by'] = User.objects.get(pk=each['updated_by']).display_name
            else:
                each['updated_by'] = ''
            each['strategy'] = Strategy.objects.get(pk=each['strategy']).name
            each['created_by'] = User.objects.get(pk=each['created_by']).display_name
            #Reformat date
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")

        return product

    def retrieve(self, request, *args, **kwargs):
        product = super().retrieve(request, *args, **kwargs)
        #reformat date
        if product.data['updated_by'] is not None:
                product.data['updated_by'] = User.objects.get(pk=product.data['updated_by']).display_name
        else:
            product.data['updated_by'] = ''
        product.data['strategy'] = Strategy.objects.get(pk=product.data['strategy']).name
        product.data['created_by'] = User.objects.get(pk=product.data['created_by']).display_name
        product.data['created_at'] = timestamp_to_strdateformat(product.data['created_at'], "%d %B %Y")
        product.data['updated_at'] = timestamp_to_strdateformat(product.data['updated_at'], "%d %B %Y")
        return product

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 1
        product = super().create(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.CREATE, TableEnum.PRODUCT)
        return product

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 1
        product = super().update(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.UPDATE, TableEnum.PRODUCT)
        return product

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 1                                 
        product = super().destroy(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.DELETE, TableEnum.PRODUCT)
        return product