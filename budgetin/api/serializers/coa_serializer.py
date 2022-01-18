from rest_framework import serializers
from api.models.coa_model import Coa


class CoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coa
        fields = '__all__'
