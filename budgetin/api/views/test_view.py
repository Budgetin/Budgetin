from rest_framework.views import APIView
from rest_framework.response import Response
<<<<<<< Updated upstream

from api.utils.listplanning import get_all_list_planning
=======
>>>>>>> Stashed changes

class TestView(APIView):
    def get(self, request):
        #print something
        return Response({})
