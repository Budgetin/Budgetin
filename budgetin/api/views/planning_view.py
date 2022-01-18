from rest_framework import viewsets
from api.models.planning_model import Planning
from api.serializers.planning_serializer import PlanningSerializer

class PlanningViewSet(viewsets.ModelViewSet):
    queryset = Planning.objects.all()
    serializer_class = PlanningSerializer
