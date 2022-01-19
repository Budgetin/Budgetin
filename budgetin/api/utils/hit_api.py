import requests
import pyDes
import binascii

from django.conf import settings

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


def get_ithc_employee_id(username):
    url = "http://employee-management-be-planalyt-dev.apps.ocpdev.dti.co.id/employees/?username__exact={}".format(
        username)
    headers = {
        "Authorization": "Api-Key {}".format(settings.ITHC_API_KEY)
    }
    res = requests.get(url, headers=headers, verify=False)
    if res.json():
        return {
            'id': res.json()[0]['id'],
        }

    return {
        'err': 'username does not exists in ITHC Employee'
    }
