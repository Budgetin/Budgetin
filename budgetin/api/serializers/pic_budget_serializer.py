from rest_framework import serializers

from api.models import PicBudget


class PicBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicBudget
        fields = '__all__'
