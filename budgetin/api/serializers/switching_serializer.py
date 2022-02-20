from rest_framework import serializers

from api.models import Switching


class SwitchingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switching
        fields = '__all__'
