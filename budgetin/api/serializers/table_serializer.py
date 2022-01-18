from rest_framework import serializers
from api.models.table_model import Table
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = '__all__'