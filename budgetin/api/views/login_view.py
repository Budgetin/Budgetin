from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from api.utils.jwt import *


class LoginView(APIView):
    def post(self, request):
        if "username" not in request.data:
            return Response({'detail': 'username must be filled'})
        if "password" not in request.data:
            return Response({'detail': 'password must be filled'})

        username = request.data['username']
        password = request.data['password']

        # Hit EAI

        # If EAI success
        # Get ITHC EmployeeID
        id = 52

        # Generate jwt
        jwt = generate_token(id, username)

        return Response({
            'token': jwt
        })
