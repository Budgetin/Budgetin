from rest_framework import serializers
from api.models.biro_model import Biro


class BiroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biro
        fields = '__all__'
