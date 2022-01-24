from api.utils.hit_api import get_employee_info
from api.models.user_model import User
from api.exceptions import NotEligibleException

def get_user_info(username):
    #Check if user exists in Budgetin DB
    users = User.objects.filter(username=username).values()
    if users:
        user = users[0]
        return user['employee_id'], user['display_name'],user['role']
    
    #Check if User S1, S2, S3
    user = get_employee_info(username)
    if user['biro_manager_id'] == user['employee_id'] or user['sub_group_manager_id'] == user['employee_id'] or user['group_manager_id'] == user['employee_id']:
        return user['employee_id'], user['display_name'], 'user'
    
    raise NotEligibleException()