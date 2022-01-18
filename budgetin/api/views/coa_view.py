from rest_framework import viewsets
from api.models.coa_model import Coa
from api.serializers.coa_serializer import CoaSerializer


class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
