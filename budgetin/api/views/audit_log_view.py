from rest_framework import viewsets, mixins
from api.models.audit_log_model import AuditLog
from api.serializers.audit_log_serializer import AuditLogSerializer


class AuditLogViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer

    # def get_queryset(self):
    #     idThing = 
    #     return super().get_queryset()
   