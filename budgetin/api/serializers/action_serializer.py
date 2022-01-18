from rest_framework import serializers
from api.models.action_model import Action


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'
