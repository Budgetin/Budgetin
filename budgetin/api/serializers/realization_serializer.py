from rest_framework import serializers

from api.models import Realization


class RealizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realization
        fields = '__all__'
