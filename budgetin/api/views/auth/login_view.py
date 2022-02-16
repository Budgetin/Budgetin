from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import User
from api.utils.jwt import generate_token
from api.utils.hit_api import get_ithc_employee_info, get_user_detail
from api.exceptions import InvalidCredentialException, NotEligibleException, NotAuthenticatedException
from api.utils.enum import RoleEnum

def is_manager(user):
    return user['biro_manager_id'] == user['employee_id'] or user['sub_group_manager_id'] == user['employee_id'] or user['group_manager_id'] == user['employee_id']

def get_admin(username):
    #Check if admin exists in Budgetin DB
    admin = User.objects.filter(username=username, role=RoleEnum.ADMIN.value).first()
    if admin:
        if not admin.is_deleted and admin.is_active:
            display_name, initial, eselon, ithc_biro = get_user_detail(username)
            return {
                'employee_id': admin.employee_id,
                'display_name': display_name,
                'role': RoleEnum.ADMIN.value,
                'initial': initial,
                'eselon': eselon,
                'ithc_biro': ithc_biro,
            }
    raise NotEligibleException()

def get_user(username):
    #Check if User is S1, S2, S3 in DB
    user = get_ithc_employee_info(username)
    print(user)
    if is_manager(user):
        return {
                'employee_id': user['employee_id'],
                'display_name': user['display_name'],
                'role': RoleEnum.USER.value,
                'initial': user['initial'],
                'eselon': user['eselon'],
                'ithc_biro': user['biro_id'],
            }
    raise NotEligibleException()

def get_user_info(username, user_type):
    
    if user_type.lower() == RoleEnum.ADMIN.value.lower():
        return get_admin(username)
    elif user_type.lower() == RoleEnum.USER.value.lower():
        return get_user(username)

class LoginView(APIView):
    def post(self, request):
        if "username" not in request.data:
            return Response({'message': 'username must be filled'})
        if "password" not in request.data:
            return Response({'message': 'password must be filled'})
        if "type" not in request.data:
            return Response({'message': 'type must be filled'})

        username = request.data['username']
        password = request.data['password']
        user_type = request.data['type']

        # # Check if users exists in Budgetin/ITHC database
        user_info = get_user_info(username, user_type)
        
        # Hit EAI
        # eai_login_status = login_eai(username, password)
        eai_login_status = "Berhasil" #DEBT

        # If EAI success, Get ITHC EmployeeID
        if eai_login_status != "Berhasil":
            raise InvalidCredentialException()
        
        # If user with given username & employee_id exists, update display_name, initial and eselon
        # Else create new user with given username, employee_id and display_name, initial and eselon 
        user, created = User.objects.update_or_create(
            username=username,
            employee_id=user_info['employee_id'],
            defaults={'display_name': user_info['display_name'],
                      'initial': user_info['initial'],
                      'eselon': user_info['eselon']
                      }
        )

        # Generate jwt
        jwt = generate_token(user.id, username, user_info['role'], user_info['eselon'], user_info['initial'], user_info['ithc_biro'])
        response = Response({
            'username': username,
            'role': user_info['role'],
            'eselon': user_info['eselon'],
            'initial': user_info['initial'],
        })
        response.set_cookie(
            key='token',
            value=jwt,
            httponly=True,
            samesite='None',
            # secure=True   
        )
                
        return response