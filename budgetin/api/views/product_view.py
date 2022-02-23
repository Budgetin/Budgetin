import pandas as pd
from io import BytesIO
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.models import Product, Strategy
from api.serializers import ProductSerializer, ProductResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import get_import_template_path
from api.utils.excel import export_excel, write_sheet
from api.exceptions import ValidationException
from api.views.upload.import_product import ImportProduct

def is_product_duplicate(product_id, product_code, product_name):
    if Product.objects.filter(product_code=product_code).exclude(id=product_id):
        raise ValidationException('Product with product code ' + product_code + ' already exists')
    if Product.objects.filter(product_name=product_name).exclude(id=product_id):
        raise ValidationException('Product with product name ' + product_name + ' already exists')

def is_product_duplicate_create(product_code, product_name):
    if Product.objects.filter(product_code=product_code):
        raise ValidationException('Product with product code' + product_code + ' already exists')
    if Product.objects.filter(product_name=product_name):
        raise ValidationException('Product with product name' + product_name + ' already exists')

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
        request.data['product_name'] = request.data['product_name'].strip()
        request.data['product_code'] = request.data['product_code'].strip()
        is_product_duplicate_create(request.data['product_code'],request.data['product_name'])
        product = super().create(request, *args, **kwargs)
        AuditLog.Save(product, request, ActionEnum.CREATE, TableEnum.PRODUCT)
        return product

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['product_name'] = request.data['product_name'].strip()
        request.data['product_code'] = request.data['product_code'].strip()
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
        return ImportProduct().start(request)
    
    @action(methods=['get'], detail=False, url_path='import/template')
    def download_import_template(self, request):
        file_path = get_import_template_path(TableEnum.PRODUCT)
        book = load_workbook(filename=file_path)

        self.write_strategy_sheet(book, file_path)

        book.close()                
        file_content = BytesIO(save_virtual_workbook(book))
        return export_excel(content=file_content, filename='import_template_product.xlsx')
    
    def write_strategy_sheet(self, book, file_path):
        columns = ['strategy_name']
        coas = self.get_all_strategy()
        dataframe = pd.DataFrame(coas, columns=columns)
        
        write_sheet(
            book=book, 
            file_path=file_path,
            dataframe=dataframe, 
            sheet_name='existing_strategy',
        )
    
    def get_all_strategy(self):
        strategies = Strategy.objects.all()
        result = []
        for strategy in strategies:
            temp = []
            temp.append(strategy.name)
            result.append(temp)
        return result