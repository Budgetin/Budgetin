from rest_framework.views import APIView
from rest_framework.response import Response

from api.utils.hit_api import get_all_biro

class BiroView(APIView):
    def get(self, request):
        biros = get_all_biro()
        biros = [biro for biro in biros if biro['manager_employee'] is not None]
        return Response(biros)