from rest_framework import viewsets

from api.models import Realization
from api.serializers import RealizationSerializer

class RealizationViewSet(viewsets.ModelViewSet):
    queryset = Realization.objects.all()
    serializer_class = RealizationSerializer
