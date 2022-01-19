from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from api.utils.jwt import *


class LoginView(APIView):
    def post(self, request):
        data = request.data
        
        return Response({
            
        })
