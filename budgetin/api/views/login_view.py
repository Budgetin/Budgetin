from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils.jwt import *
from api.utils.hit_api import login_eai
from api.models.user_model import User
from api.utils.user import get_user_info
from api.exceptions import InvalidCredentialException

class LoginView(APIView):
    def post(self, request):
        if "username" not in request.data:
            return Response({'message': 'username must be filled'})
        if "password" not in request.data:
            return Response({'message': 'password must be filled'})

        username = request.data['username']
        password = request.data['password']

        # # Check if users exists in Budgetin database
        employee_id, display_name, role, eselon = get_user_info(username)

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
        })
        response.set_cookie(
            key='token',
            value=jwt,
            httponly=True,
            samesite='None',
            secure=True   
        )
                
        return response
