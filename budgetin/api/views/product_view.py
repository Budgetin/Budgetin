from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets
from rest_framework.response import Response

from api.permissions import IsAuthenticated, IsAdmin
from api.models import Product,Strategy,User
from api.serializers import ProductSerializer, ProductResponseSerializer
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.exceptions.validation_exception import ValidationException

def is_product_duplicate(product_id, product_code, product_name):
    if Product.objects.filter(product_code=product_code).exclude(id=product_id) or Product.objects.filter(product_name=product_name).exclude(id=product_id):
        raise ValidationException

def is_product_duplicate_create(product_code, product_name):
    if Product.objects.filter(product_code=product_code).exclude(product_name=product_name) or Product.objects.filter(product_name=product_name).exclude(product_code=product_code):
        raise ValidationException


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.all_object.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        queryset = Product.objects.select_related('strategy', 'created_by', 'updated_by').all()
        for product in queryset:
            product.format_timestamp("%d %B %Y")

        serializer = ProductResponseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        product = Product.objects.select_related('strategy', 'created_by', 'updated_by').get(pk=kwargs['pk'])
        product.format_timestamp("%d %B %Y")
        
        serializer = ProductResponseSerializer(product, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.custom_user['id']
        is_product_duplicate_create(request.data['product_code'],request.data['product_name'])
        product = super().create(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.CREATE, TableEnum.PRODUCT)
        return product

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        is_product_duplicate(kwargs['pk'],request.data['product_code'],request.data['product_name'])
        product = super().update(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.UPDATE, TableEnum.PRODUCT)
        return product

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']                       
        product = super().destroy(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.DELETE, TableEnum.PRODUCT)
        return product