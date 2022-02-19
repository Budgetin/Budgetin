import pandas as pd
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.models import Product, Strategy
from api.serializers import ProductSerializer, ProductResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_excel, read_file
from api.exceptions import ValidationException

def is_product_duplicate(product_id, product_code, product_name):
    if Product.objects.filter(product_code=product_code).exclude(id=product_id) or Product.objects.filter(product_name=product_name).exclude(id=product_id):
        raise ValidationException('Product ' + product_code + ' already exists')

def is_product_duplicate_create(product_code, product_name):
    if Product.objects.filter(product_code=product_code) or Product.objects.filter(product_name=product_name):
        raise ValidationException('Product ' + product_code + ' already exists')


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.all_object.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

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

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        is_product_duplicate_create(request.data['product_code'],request.data['product_name'])
        product = super().create(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.CREATE, TableEnum.PRODUCT)
        return product

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        is_product_duplicate(kwargs['pk'],request.data['product_code'],request.data['product_name'])
        product = super().update(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.UPDATE, TableEnum.PRODUCT)
        return product

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']                       
        product = super().destroy(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.DELETE, TableEnum.PRODUCT)
        return product
    
    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='import')
    def import_from_excel(self, request):
        file = read_file(request)
        df = read_excel(file, 'product')
        errors = []
        
        for index, row in df.iterrows():
            print(index)
            errors.extend(self.insert_to_db(request, row, (index+2)))
        
        if errors:
            raise ValidationException(errors)

        return Response(status=204)    

    def insert_to_db(self, request, data, index):
        errors = []
        
        code = data['product_code']
        if self.product_already_exists(code):
            errors.append("Product '{}' at line {} already exists".format(code, index))
        
        ''' 
        Get strategy. Strategy Can be empty. If filled, strategy must exists in DB.
        '''
        strategy_name = data['strategy_name']
        if pd.isnull(strategy_name):
            strategy = None
        elif self.strategy_not_exists(strategy_name, index):
            errors.append("Strategy '{}' at line {} does not exists".format(strategy_name, index))
        else:
            strategy = Strategy.objects.filter(name__iexact=strategy_name).first()
            
        if not errors:
            product = self.create_product(request, data, strategy)
            AuditLog.Save(ProductSerializer(product), request, ActionEnum.CREATE, TableEnum.PRODUCT) 
        
        return errors
            
    def product_already_exists(self, code):
        return Product.objects.filter(product_code__iexact=code).count() > 0
    
    def strategy_not_exists(self, name, index):
        return Strategy.objects.filter(name__iexact=name).count() == 0
    
    def create_product(self, request, data, strategy):
        return Product.objects.create(
            product_code = data['product_code'],
            product_name = data['product_name'],
            strategy = strategy,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )