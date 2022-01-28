from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils.hit_api import get_all_biro

class BiroView(APIView):
    def get(self, request):
        biros = get_all_biro()
        
        # Biro that lasts with * will not be returned. e.g: NIS*, IBO*
        biros = [biro for biro in biros if biro['code'][-1] != '*']
        return Response(biros)