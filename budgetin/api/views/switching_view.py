from rest_framework import viewsets

from api.models import Switching
from api.serializers import SwitchingSerializer

class RealizationViewSet(viewsets.ModelViewSet):
    queryset = Switching.objects.all()
    serializer_class = SwitchingSerializer
