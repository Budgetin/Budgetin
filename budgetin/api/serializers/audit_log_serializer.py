from rest_framework import serializers
from api.models.audit_log_model import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = '__all__'