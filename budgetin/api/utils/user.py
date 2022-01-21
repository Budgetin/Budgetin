from api.utils.hit_api import get_employee_info
from api.models.pic_budget_model import PicBudget
from api.models.user_model import User

def user_has_access(username):
    #Check if Admin
    user = User.objects.filter(username=username)
    if user and user.values()[0]['role'] == 'admin':
        return True
    
    #Check if User S1, S2, S3
    data_check = get_employee_info(username)
    if 'err' in data_check:
        return False
    if data_check['biro_manager_id'] == data_check['employee_id'] or data_check['sub_group_manager_id'] == data_check['employee_id'] or data_check['group_manager_id'] == data_check['employee_id']:
        return True
    
    #Check if User is PIC
    pic_budget = PicBudget.objects.filter(employee_id=data_check['employee_id'])
    if pic_budget:
        return True
    
    #No Access
    return False