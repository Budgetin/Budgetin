import requests
import pyDes
import binascii

from django.conf import settings
from api.exceptions import *

# Encrypt Password dengan 3DES untuk Login EAI
def encrypt_password_3des_eai(password):
    key = settings.EAI_PUBLIC_KEY
    triple_des = pyDes.triple_des(
        key, pyDes.ECB, pad=None, padmode=pyDes.PAD_PKCS5)

    encrypted = triple_des.encrypt(password)
    encrypted_password = binascii.hexlify(encrypted).decode('utf-8')

    return encrypted_password

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
    "password": "''' + encrypt_password_3des_eai(password) + '''"
    }'''

    response_login = requests.post(
        url_login, data=body_login, headers=headers_login, verify=False)

    return response_login.json()['error_schema']['error_message']['indonesian']

#Get Employee ID from Username
def get_ithc_employee_id(username):
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/employees/?username__exact={}".format(
        username)
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        # check for user that is not deleted
        user = [u for u in res.json() if u['is_deleted'] == False]
        if user:
            return {
                'id': user[0]['id'],
            }
    raise NotFoundException()

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
    raise NotFoundException()

#Get S4
def get_s4():
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/employees/?eselon__exact=5"
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        temp = []
        for each in res.json():
            user_id = each['id']
            display_name = each['display_name']
            username = each['username']
            employee_json = {
                'id' : user_id,
                'name' : display_name,
                'username' : username
            }
            temp.append(employee_json)
        return temp
    raise NotFoundException()

#Get Biro Information
def get_biro_info(biro_id):
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/biros/?include=sub_group,sub_group.group,sub_group.group.divisi&id__exact={}".format(
        biro_id)
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        #check for biro that is not deleted
        biro = [b for b in res.json() if b['is_deleted'] == False]
        if biro:
            biro_manager_id = biro[0]['manager_employee']
            sub_group_id = biro[0]['sub_group']['id']
            sub_group_manager_id = biro[0]['sub_group']['manager_employee']
            group_id = biro[0]['sub_group']['group']['id']
            group_manager_id = biro[0]['sub_group']['group']['manager_employee']
            divisi_id = biro[0]['sub_group']['group']['divisi']['id']
            return {
                'biro_id' : biro_id,
                'biro_manager_id' : biro_manager_id,
                'sub_group_id' : sub_group_id,
                'sub_group_manager_id' : sub_group_manager_id,
                'group_id' : group_id,
                'group_manager_id' : group_manager_id,
                'divisi_id' : divisi_id
            }
    raise NotFoundException()
    

#Get Employee Information
def get_employee_info(username):
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/employees/?include=biro,sub_group,sub_group.group,sub_group.group.divisi&username__exact={}".format(
        username)
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        #check for employee that is not deleted
        employee = [e for e in res.json() if e['is_deleted'] == False]
        if employee:
            employee_id = employee[0]['id']
            biro_id = employee[0]['biro']
            display_name = employee[0]['display_name']
            biro_manager_id = employee[0]['biro']['manager_employee']
            sub_group_id = employee[0]['sub_group']['id']
            sub_group_manager_id = employee[0]['sub_group']['manager_employee']
            group_id = employee[0]['sub_group']['group']['id']
            group_manager_id = employee[0]['sub_group']['group']['manager_employee']
            divisi_id = employee[0]['sub_group']['group']['divisi']['id']
            return {
                'employee_id' : employee_id,
                'display_name' : display_name, 
                'biro_id' : biro_id,
                'biro_manager_id' : biro_manager_id,
                'sub_group_id' : sub_group_id,
                'sub_group_manager_id' : sub_group_manager_id,
                'group_id' : group_id,
                'group_manager_id' : group_manager_id,
                'divisi_id' : divisi_id
            }
    raise NotEligibleException()