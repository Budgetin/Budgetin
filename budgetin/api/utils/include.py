from api.models.user_model import User
from api.models.strategy_model import Strategy


def include(param, paramid):
    if param == "strategy":
        return Strategy.objects.filter(id=paramid).values()[0]

    if param == "created_by":
        user = User.objects.filter(id=1).values()[0]
        return {
            "id" : user['id'],
            'employee_id' : user['employee_id'],
            'display_name' : user['display_name'],
            'username' : user['username']
        }
