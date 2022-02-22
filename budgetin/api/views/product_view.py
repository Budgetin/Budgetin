from django.forms import model_to_dict
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
from api.models import Product, Strategy, User
from api.serializers import ProductSerializer, ProductResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_file, get_import_template_path
from api.utils.excel import read_excel, export_excel, write_sheet, export_errors_as_excel, is_empty
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
            errors = self.insert_to_db(request, data, (index+2), errors)
        
        if errors:
            return export_errors_as_excel(errors)

        return Response(status=204)    

    def insert_to_db(self, request, data, index, errors):
        errors.extend(self.validate_data(data, index))

        if not errors:
            strategy = self.get_strategy(data)
            self.create_or_update_product(request, data, strategy)
        
        return errors
    
    def validate_data(self, data, index):
        errors = []
        errors = self.validate_product(data, index, errors)
        errors = self.validate_strategy(data, index, errors)
        return errors
    
    def validate_product(self, data, index, errors):
        code = data['product_code']
        name = data['product_name']
        
        if is_empty(code):
            errors.append("Row {} - Product code must be filled".format(index))
            
        if is_empty(name):
            errors.append("Row {} - Product name must be filled".format(index))

        return errors
    
    def validate_strategy(self, data, index, errors):
        strategy_name = data['strategy_name']
        if not is_empty(strategy_name) and not Strategy.name_exists(strategy_name):
            errors.append("Row {} - Strategy '{}' does not exists".format(index, strategy_name))
        return errors
    
    def get_strategy(self, data):
        strategy_name = data['strategy_name']
        if is_empty(strategy_name):
            strategy, _ = Strategy.objects.get_or_create(name='None')
        else:
            strategy = Strategy.objects.filter(name__iexact=strategy_name).first()
        return strategy
    
    def create_or_update_product(self, request, data, strategy):
        new_product_dict = {
            'product_code': data['product_code'],
            'product_name' : data['product_name'],
            'strategy': strategy,
            'updated_by': User.objects.get(pk=request.custom_user['id'])
        }
        
        new_product = Product(**new_product_dict)
        product = Product.objects.filter(product_code=data['product_code']).first()
        if not product:
            self.create_new_product(request, new_product)
        elif product and not product.equal(new_product):
            self.update_product(request, product, new_product_dict)
    
    def create_new_product(self, request, new_product):
        new_product.created_by = new_product.updated_by
        new_product.save()
        AuditLog.Save(ProductSerializer(new_product), request, ActionEnum.CREATE, TableEnum.PRODUCT)         
    
    def update_product(self, request, product, new_product):
        product = self.update_fields(product, new_product)
        product.save()
        AuditLog.Save(ProductSerializer(product), request, ActionEnum.UPDATE, TableEnum.PRODUCT) 

    def update_fields(self, model, new_model_dict):
        for key, value in new_model_dict.items():
            setattr(model, key, value)
        return model
    
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