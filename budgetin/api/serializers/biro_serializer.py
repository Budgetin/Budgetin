from rest_framework import serializers

from api.models import Biro


class BiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biro
        fields = '__all__'
