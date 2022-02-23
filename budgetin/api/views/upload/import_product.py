from django.utils.translation import ugettext_lazy as _
from rest_framework.response import Response

from api.models import Product, Strategy, User
from api.serializers import ProductSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.file import read_file
from api.utils.excel import read_excel, export_errors_as_excel, is_empty

class ImportProduct():
    def start(self, request):
        file = read_file(request)
        df = read_excel(file, TableEnum.PRODUCT.value)
        
        # Retrieve data from DB and convert it to Key, Value dictionary.
        # This is done to reduce DB calls and optimize searching for specified key with O(1) complexity when searching 
        # e.g for product: {'ba001': product (obj), 'ba002': product(obj)}
        strategies = dict((strategy.name.lower(), strategy) for strategy in Strategy.objects.all())
        products = dict((product.product_code.lower(), product) for product in Product.objects.all())
        user = User.objects.get(pk=request.custom_user['id'])
        
        errors = []
        for index, data in df.iterrows():
            errors = self.validate_product(data, index+2, errors)
            strategy, errors = self.get_strategy(data, index+2, errors, strategies)
            
            if not errors:
                products = self.create_or_update_product(request, data, user, strategy, products)

        
        if errors:
            return export_errors_as_excel(errors)

        return Response(status=204)    
    
    def validate_product(self, data, index, errors):
        code = data['product_code']
        name = data['product_name']
        
        if is_empty(code):
            errors.append("Row {} - Product code must be filled".format(index))
            
        if is_empty(name):
            errors.append("Row {} - Product name must be filled".format(index))

        return errors
    
    def get_strategy(self, data, index, errors, strategies):
        strategy_name = data['strategy_name']
        if is_empty(strategy_name):
            strategy = strategies['none']
        else:
            strategy_name = strategy_name.strip()
            if strategy_name.lower() not in strategies:
                errors.append("Row {} - Strategy '{}' does not exists".format(index, strategy_name))
                return _, errors
            else:
                strategy = strategies[strategy_name.lower()]
        return strategy, errors
    
    def create_or_update_product(self, request, data, user, strategy, products):
        product_code = data['product_code'].strip()
        product_name = data['product_name'].strip()
        update_dict = {
            'product_name' : product_name,
            'strategy': strategy,
            'updated_by': user
        }
        
        new_product = Product(
            product_code = data['product_code'],
            **update_dict
        )
        
        if product_code.lower() not in products:
            product = self.create_new_product(request, new_product)
        else:
            product = products[product_code.lower()]
            if not product.equal(new_product):
                product = self.update_product(request, product, update_dict)
        
        products[product_code.lower()] = product
        return products
    
    def create_new_product(self, request, new_product):
        new_product.created_by = new_product.updated_by
        new_product.save()
        AuditLog.Save(ProductSerializer(new_product), request, ActionEnum.CREATE, TableEnum.PRODUCT)         
    
    def update_product(self, request, product, update_dict):
        product = self.update_fields(product, update_dict)
        product.save()
        AuditLog.Save(ProductSerializer(product), request, ActionEnum.UPDATE, TableEnum.PRODUCT) 

    def update_fields(self, model, update_dict):
        for key, value in update_dict.items():
            setattr(model, key, value)
        return model