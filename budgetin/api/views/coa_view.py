from rest_framework import viewsets
from api.models.coa_model import Coa
from api.serializers.coa_serializer import CoaSerializer
from api.permissions import IsAuthenticated, IsAdmin


class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    # def create(self, request):
    #     creatd_by = request.custom_user['id']
