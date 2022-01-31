from rest_framework import serializers

from api.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    modified_by = serializers.CharField()
    serialized_data = serializers.DictField()
    class Meta:
        model = AuditLog
        fields = '__all__'