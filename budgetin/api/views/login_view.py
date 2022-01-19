from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from api.utils.jwt import *


class LoginView(APIView):
    def get(self, request):
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImJhbWJhbmciLCJpYXQiOjE2NDI1ODY5NjcsImV4cCI6MTY0MTk4MjE2N30.LwKe9w0nn7Fq6yb8xV-L6-MD7qilCysai0wFysJOc0E'
        payload = decode_token(token)

        return Response({
            'payload': payload,
        })

    # def get(self, request):
    #     token = generate_token()

    #     return Response({
    #         'token': token,
    #     })
