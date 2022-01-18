from rest_framework import serializers
from api.models.pic_budget_model import PicBudget


class PicBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PicBudget
        fields = '__all__'
