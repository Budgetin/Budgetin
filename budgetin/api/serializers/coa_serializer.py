from rest_framework import serializers

from api.models import Coa


class CoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coa
        fields = '__all__'
