from rest_framework.views import APIView
from rest_framework.response import Response

from api.permissions import IsAuthenticated

class LoginUserView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(request.custom_user)