from rest_framework.views import APIView
from rest_framework.response import Response

from api.permissions import IsAuthenticated
from api.exceptions import NotAuthenticatedException

class LoginUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        role = request.query_params['role']
        if role.lower() != request.custom_user['role'].lower():
            raise NotAuthenticatedException()
        
        return Response(request.custom_user)