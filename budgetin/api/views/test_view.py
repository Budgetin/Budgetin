from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils.biro import create_update_all_biro

class TestView(APIView):
    def get(self, request):
        create_update_all_biro()
        return Response({})
