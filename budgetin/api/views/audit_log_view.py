from rest_framework import viewsets, mixins
from api.models.audit_log_model import AuditLog
from api.serializers.audit_log_serializer import AuditLogSerializer


class AuditLogViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    
    
    
# def get_queryset(self):
#     if self.request.method == 'GET':
#         tableid = self.request.GET.get('table_id', None)
#         entityid = self.request.GET.get('entity_id', None)
#         if tableid is not None and entityid is not None:
#             queryset = AuditLog.objects.filter(entity_id=entityid).filter(table_id=tableid)
#         else:
#             queryset = None
#     return queryset
    
