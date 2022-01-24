from api.models.user_model import User
from api.models import Strategy, Product


def include(param, paramid):
    arrParam = param.split(".")
    if arrParam[0] == "strategy":
        return Strategy.objects.filter(id=paramid).values()[0]

    if arrParam[0] == "created_by" or arrParam[0] == "updated_by":
        user = User.objects.filter(id=paramid).values()[0]
        return {
            'id' : user['id'],
            'employee_id' : user['employee_id'],
            'display_name' : user['display_name'],
            'username' : user['username']
        }
    
    if arrParam[0] == "product":
        if len(arrParam)==2 and arrParam[1] == "strategy":
            product = Product.objects.filter(id=paramid).values()[0]
            strategy = include("strategy",product['strategy_id'])
            return {
                'id' : product['id'],
                'name' : product['product_name'],
                'status' : product['is_active'],
                'strategy' : strategy
            }
        else:
            product = Product.objects.filter(id=paramid).values()[0]
            return {
                'id' : product['id'],
                'name' : product['product_name'],
                'status' : product['is_active'],
                'strategy' : product['strategy_id']
            }
