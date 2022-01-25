from api.models.user_model import User
from api.models import Strategy, Product


            # #include strategy in list
            # if request.query_params:
            #     params = request.query_params.getlist('include')[0].split(",")
            #     for param in params:
            #         paramSplitted = param.split(".")[0]
            #         param_name = paramSplitted.lower()
            #         paramid = each[param_name]
            #         included_data = include(param, paramid)
            #         each[param_name] = included_data


                    #include strategy in retrieve
        # if request.query_params:
        #         #include strategy
        #         if request.query_params:
        #             params = request.query_params.getlist('include')[0].split(",")
        #             for param in params:
        #                 paramSplitted = param.split(".")[0]
        #                 param_name = paramSplitted.lower()
        #                 paramid = product.data[param_name]
        #                 included_data = include(param, paramid)
        #                 product.data[param_name] = included_data

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
