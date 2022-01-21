from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from api.utils.jwt import *
from api.utils.hit_api import login_eai
from api.utils.hit_api import get_ithc_employee_id
from api.models.user_model import User
from api.utils.user import user_has_access

class LoginView(APIView):
    def post(self, request):
        if "username" not in request.data:
            return Response({'detail': 'username must be filled'})
        if "password" not in request.data:
            return Response({'detail': 'password must be filled'})

        username = request.data['username']
        password = request.data['password']

        # # Check if users exists in Budgetin database
        # user = User.objects.filter(username=username)
        # if not user:
        #     return Response({
        #         "message": "You don't have permission to access this site",
        #     })
        # role = user.values()[0]['role']

        if not user_has_access(username):
            return Response({
                'message' : "You don't have access"
            })

        # Hit EAI
        eai_login_status = login_eai(username, password)

        # If EAI success
        # Get ITHC EmployeeID
        if eai_login_status != "Berhasil":
            return Response({
                "message": "invalid username/password"
            })

        # Get Employee ID from ITHC Employee table
        res = get_ithc_employee_id(username)
        if 'err' in res:
            return Response({
                "message": res['err']
            })

        id = res['id']

        # Generate jwt
        jwt = generate_token(id, username, 'user')

        return Response({
            'token': jwt,
        })
