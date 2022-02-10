import requests

from django.conf import settings

from api.exceptions import *
from api.utils.triple_des import encrypt_3des


# Login EAI
def login_eai(username, password):
    url_token = "https://sso-apigw-int.dti.co.id/auth/realms/3scale-dev/protocol/openid-connect/token"
    headers_token = {"Content-Type": "application/x-www-form-urlencoded"}
    body_token = 'grant_type=client_credentials&client_id={}&client_secret={}'.format(
        settings.EAI_CLIENT_ID, settings.EAI_CLIENT_SECRET)
    response_token = requests.post(
        url_token, data=body_token, headers=headers_token, verify=False)
    access_token = response_token.json()['access_token']

    url_login = "https://api.devapps.ocp.dti.co.id/eai/ad-gateway/v2/api/verify"
    headers_login = {"x-source-client-id": settings.EAI_X_SOURCE_CLIENT_ID,
                     "x-source-transaction-id": "BUDGETIN-1234567890qwertyuiopasdfghjklzxc",
                     "Authorization": "Bearer " + access_token,
                     "Content-Type": "application/json"}
    body_login = '''{
    "application_id": "Budgetin",
    "user_id": "''' + username + '''",
    "password": "''' + encrypt_3des(password, settings.EAI_PUBLIC_KEY) + '''"
    }'''

    response_login = requests.post(
        url_login, data=body_login, headers=headers_login, verify=False)

    return response_login.json()['error_schema']['error_message']['indonesian']


#Get IMO D Employee
def get_imo_d_employee():
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/employees/?biro__code__exact=IMO D"
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        data = []
        for each in res.json():
            if each['status_employee'] == 1:
                user_id = each['id']
                display_name = each['display_name']
                username = each['username']
                employee_json = {
                    'id' : user_id,
                    'name' : display_name,
                    'username' : username
                }
                data.append(employee_json)
        return data
    raise NotFoundException('IMO Employee')


#Get All Biro
def get_all_biro(params=''):
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/biros/"
    if params != '':
        url += '?include=' + params
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        #check for biro that is not deleted
        biro = [b for b in res.json() if b['is_deleted'] == False]
        if biro:
            return biro
    raise NotFoundException('Biro')


#Get Employee Information
def get_ithc_employee_info(username):
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/employees/?include=biro,sub_group,sub_group.group,sub_group.group.divisi,eselon&username__exact={}".format(
        username)
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        #check for employee that is not deleted
        employee = [e for e in res.json() if e['is_deleted'] == False]
        eselon = ''
        if employee:
            employee_id = employee[0]['id']
            display_name = employee[0]['display_name']
            if employee[0]['eselon']:
                eselon = employee[0]['eselon']['code']
            biro_id = employee[0]['biro']
            if biro_id:
                biro_manager_id = employee[0]['biro']['manager_employee']
            sub_group_id = employee[0]['sub_group']['id']
            if sub_group_id:            
                sub_group_manager_id = employee[0]['sub_group']['manager_employee']
            group_id = employee[0]['sub_group']['group']['id']
            if group_id:
                group_manager_id = employee[0]['sub_group']['group']['manager_employee']
            divisi_id = employee[0]['sub_group']['group']['divisi']['id']
            initial = employee[0]['initial']
            return {
                'employee_id' : employee_id,
                'eselon': eselon,
                'display_name' : display_name, 
                'biro_id' : biro_id,
                'biro_manager_id' : biro_manager_id,
                'sub_group_id' : sub_group_id,
                'sub_group_manager_id' : sub_group_manager_id,
                'group_id' : group_id,
                'group_manager_id' : group_manager_id,
                'divisi_id' : divisi_id,
                'initial': initial,
            }
    raise EmployeeNotFoundException()

def get_user_detail(username):
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/employees/?include=eselon&username__exact={}".format(
        username)
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        employee = [e for e in res.json() if e['is_deleted'] == False]
        if employee:
            return employee[0]['display_name'], employee[0]['initial'], employee[0]['eselon']['code']