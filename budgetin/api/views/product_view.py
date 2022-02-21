import pandas as pd
from io import BytesIO
from django.utils.translation import ugettext_lazy as _
from django.db import transaction
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from openpyxl import load_workbook
from openpyxl.writer.excel import save_virtual_workbook

from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.models import Product, Strategy, Coa
from api.serializers import ProductSerializer, ProductResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_excel, read_file, get_import_template_path, remove_sheet, export_excel
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
        df = read_excel(file, TableEnum.PRODUCT.value)
        errors = []
        
        for index, data in df.iterrows():
            errors.extend(self.insert_to_db(request, data, (index+2)))
        
        if errors:
            raise ValidationException(errors)

        return Response(status=204)    

    def insert_to_db(self, request, data, index):
        errors = self.validate_data(data, index)

        if not errors:
            strategy = self.get_strategy(data)
            product = self.create_product(request, data, strategy)
            AuditLog.Save(ProductSerializer(product), request, ActionEnum.CREATE, TableEnum.PRODUCT) 
        
        return errors
    
    def validate_data(self, data, index):
        errors = []
        errors = self.validate_product(data, index, errors)
        errors = self.validate_strategy(data, index, errors)
        return errors
    
    def validate_product(self, data, index, errors):
        code = data['product_code']
        name = data['product_name']
        
        if pd.isnull(code):
            errors.append("Row {} - Product code must be filled".format(index))
        elif Product.code_exists(code):
            errors.append("Row {} - Product code '{}' already exists".format(index, code))
            
        if pd.isnull(name):
            errors.append("Row {} - Product name must be filled".format(index))
        elif Product.name_exists(name):
            errors.append("Row {} - Product '{}' already exists".format(index, name))

        return errors
    
    def validate_strategy(self, data, index, errors):
        strategy_name = data['strategy_name']
        if not pd.isnull(strategy_name) and not Strategy.name_exists(strategy_name):
            errors.append("Row {} - Strategy '{}' does not exists".format(index, strategy_name))
        return errors
    
    def get_strategy(self, data):
        strategy_name = data['strategy_name']
        if pd.isnull(strategy_name):
            strategy = None
        else:
            strategy = Strategy.objects.filter(name__iexact=strategy_name).first()
        return strategy
    
    def create_product(self, request, data, strategy):
        return Product.objects.create(
            product_code = data['product_code'],
            product_name = data['product_name'],
            strategy = strategy,
            created_by_id = request.custom_user['id'],
            updated_by_id = request.custom_user['id'],
        )
    
    @action(methods=['get'], detail=False, url_path='import/template')
    def download_import_template(self, request):
        file_path = get_import_template_path(TableEnum.PRODUCT)
        book = load_workbook(filename=file_path)

        self.write_coa_sheet(book, file_path)

        book.close()                
        return export_excel(content=BytesIO(save_virtual_workbook(book)), filename='import_template_product.xlsx')
    
    def write_coa_sheet(self, book, file_path):
        columns = ['coa_name', 'hyperion_name', 'coa_definition']
        coas = self.get_all_coa()
        
        writer = pd.ExcelWriter(file_path, engine = 'openpyxl')
        writer.book = book
        
        if 'existing_coa' in book.sheetnames:
            remove_sheet(book, 'existing_coa')            
            
        df = pd.DataFrame(coas, columns=columns)
        df.to_excel(writer, sheet_name = 'existing_coa', index=False)
        writer.save()
        writer.close()
    
    def get_all_coa(self):
        coas = Coa.objects.all()
        result = []
        for coa in coas:
            temp = []
            temp.append(coa.name)
            temp.append(coa.hyperion_name)
            temp.append(coa.definition)
            result.append(temp)
        return result