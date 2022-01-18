from rest_framework import viewsets
from api.models.action_model import Action
from api.serializers.action_serializer import ActionSerializer


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Action.objects.all()
    serializer_class = ActionSerializer
