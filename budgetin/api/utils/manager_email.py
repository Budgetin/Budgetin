from api.utils.hit_api import get_all_biro

def get_managers_email(biro_id, biros=''):
    if biros == '':
        biros = biros=get_all_biro('manager_employee,sub_group,sub_group.group,manager_employee,sub_group.manager_employee,sub_group.group.manager_employee')
    email_list = []
    biro = [biro for biro in biros if biro['id'] == biro_id]
    if biro:
        if biro[0]['manager_employee']:
            email_list.append(biro[0]['manager_employee']['work_email'])
        if biro[0]['sub_group']['manager_employee']:
            email_list.append(biro[0]['sub_group']['manager_employee']['work_email'])
        if biro[0]['sub_group']['group']['manager_employee']:
            email_list.append(biro[0]['sub_group']['group']['manager_employee']['work_email'])
            
    return email_list
    
    
        
    