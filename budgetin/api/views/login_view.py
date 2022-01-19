from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from api.utils.jwt import *
from api.utils.hit_api import login_eai
from api.utils.hit_api import get_ithc_employee_id


class LoginView(APIView):
    def post(self, request):
        if "username" not in request.data:
            return Response({'detail': 'username must be filled'})
        if "password" not in request.data:
            return Response({'detail': 'password must be filled'})

        username = request.data['username']
        password = request.data['password']

        # Hit EAI
        login_status = login_eai(username, password)

        # If EAI success
        # Get ITHC EmployeeID
        if login_status != "Berhasil":
            return Response({
                "detail": "invalid username/password"
            })

        res = get_ithc_employee_id(username)
        if 'err' in res:
            return Response({
                "detail": res['err']
            })
        id = res['id']

        # Generate jwt
        jwt = generate_token(id, username)

        return Response({
            'token': jwt,
        })
