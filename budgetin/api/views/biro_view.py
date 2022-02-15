from rest_framework import viewsets

from api.models import Biro
from api.serializers import BiroSerializer
from api.permissions import IsAuthenticated, IsAdmin

class BiroViewSet(viewsets.ModelViewSet):
    queryset = Biro.objects.all()
    serializer_class = BiroSerializer
    permission_classes = [IsAuthenticated, IsAdmin]