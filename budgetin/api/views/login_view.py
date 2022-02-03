from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import User
from api.utils.jwt import generate_token, decode_token
from api.utils.hit_api import login_eai, get_ithc_employee_info, get_initial_and_eselon
from api.exceptions import InvalidCredentialException, NotEligibleException
from api.utils.enum import RoleEnum

def get_user_info(username):
    #Check if user exists in Budgetin DB
    users = User.objects.filter(username=username).values()
    if users:
        user = users[0]
        if user["is_deleted"] == False:
            initial, eselon = get_initial_and_eselon(username)
            return user['employee_id'], user['display_name'], user['role'], initial, eselon
    
    #Check if User S1, S2, S3
    user = get_ithc_employee_info(username)
    if user['biro_manager_id'] == user['employee_id'] or user['sub_group_manager_id'] == user['employee_id'] or user['group_manager_id'] == user['employee_id']:
        return user['employee_id'], user['display_name'], RoleEnum.USER.value, user['initial'], user['eselon']
    
    raise NotEligibleException()

class LoginView(APIView):
    def post(self, request):
        if "username" not in request.data:
            return Response({'message': 'username must be filled'})
        if "password" not in request.data:
            return Response({'message': 'password must be filled'})

        username = request.data['username']
        password = request.data['password']

        # # Check if users exists in Budgetin/ITHC database
        employee_id, display_name, role, initial, eselon = get_user_info(username)

        # Hit EAI
        eai_login_status = login_eai(username, password)

        # If EAI success, Get ITHC EmployeeID
        if eai_login_status != "Berhasil":
            raise InvalidCredentialException()
        
        # If user with given username & employee_id exists, update display_name
        # Else create new user with given username, employee_id and display_name
        user, created = User.objects.update_or_create(
            username=username,
            employee_id=employee_id,
            defaults={'display_name': display_name}
        )

        # Generate jwt
        jwt = generate_token(user.id, username, role, eselon)
        response = Response({
            'username': username,
            'display_name': display_name,
            'role': role,
            'initial': initial,
        })
        response.set_cookie(
            key='token',
            value=jwt,
            httponly=True,
            samesite='None',
            secure=True   
        )
                
        return response
