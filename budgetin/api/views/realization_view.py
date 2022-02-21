from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Realization
from api.serializers import RealizationSerializer, RealizationResponseSerializer

class RealizationViewSet(viewsets.ModelViewSet):
    queryset = Realization.objects.all()
    serializer_class = RealizationSerializer

    def list(self, request, *args, **kwargs):
        queryset = Realization.objects.all()

        serializer = RealizationResponseSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        queryset = Realization.objects.get(pk=kwargs['pk'])
        
        serializer = RealizationResponseSerializer(queryset, many=False)
        return Response(serializer.data)
