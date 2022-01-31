from rest_framework import serializers

from api.models import Coa


class CoaSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField()
    updated_by = serializers.CharField()
    class Meta:
        model = Coa
        fields = '__all__'
