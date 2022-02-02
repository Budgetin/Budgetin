from rest_framework import serializers

from api.models import Budget, Coa


class BudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budget
        fields = '__all__'

class CoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coa
        fields = ['id', 'name']

class BudgetResponseSerializer(serializers.ModelSerializer):
    coa = CoaSerializer(many=False)
    class Meta:
        model = Budget
        fields = ['id', 'expense_type', 'planning_q1', 'planning_q2', 'planning_q3', 'planning_q4', 
                  'realization_jan', 'realization_feb', 'realization_mar', 'realization_apr', 'realization_may',
                  'realization_jun', 'realization_jul', 'realization_aug', 'realization_sep', 'realization_oct',
                  'realization_nov', 'realization_dec', 'switching_in', 'switching_out', 'top_up', 'returns',
                  'allocate', 'coa']