from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils.listplanning import get_all_list_planning

class TestView(APIView):
    def get(self, request):
        #print something
        get_all_list_planning()
        return Response({})
