from django.db.models import Q
from api.utils.enum import SwitchingTypeEnum
from rest_framework import serializers

from api.models import Realization, Switching


class RealizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Realization
        fields = '__all__'

class RealizationResponseSerializer(serializers.ModelSerializer):
    switching_in = serializers.SerializerMethodField()
    switching_out = serializers.SerializerMethodField()
    top_up = serializers.SerializerMethodField()
    returns = serializers.SerializerMethodField()

    class Meta:
        model = Realization
        exclude = ['is_deleted', 'deleted_at', 'created_at', 'updated_at', 'created_by', 'updated_by']

    def get_switching_in(self, realization):
        sw_in = Switching.objects.filter(to_plus=realization.budget_id).filter(Q(type=SwitchingTypeEnum.SWITCH_IN.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_IN.value))
        total = 0
        for each in sw_in:
            total += each.nominal
        return total
    
    def get_switching_out(self, realization):
        sw_out = Switching.objects.filter(from_minus=realization.budget_id).filter(Q(type=SwitchingTypeEnum.SWITCH_OUT.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_OUT.value))
        total = 0
        for each in sw_out:
            total += each.nominal
        return total

    def get_top_up(self, realization):
        sw_out = Switching.objects.filter(to_plus=realization.budget_id).filter(Q(type=SwitchingTypeEnum.TOPUP.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_OUT.value))
        total = 0
        for each in sw_out:
            total += each.nominal
        return total
    
    def get_returns(self, realization):
        sw_out = Switching.objects.filter(from_minus=realization.budget_id).filter(Q(type=SwitchingTypeEnum.RETURN.value) | Q(type=SwitchingTypeEnum.CORRECTION_SWITCHING_OUT.value))
        total = 0
        for each in sw_out:
            total += each.nominal
        return total