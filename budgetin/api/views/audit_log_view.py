from rest_framework import viewsets, mixins
from api.models import AuditLog, User
from api.serializers.audit_log_serializer import AuditLogSerializer
from rest_framework.response import Response
from api.utils.date_format import timestamp_to_strdateformat

class AuditLogViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    
    def list(self, request, *args, **kwargs):
        param_table = request.GET.get('table')
        param_entity = request.GET.get('entity')

        if param_table and param_entity:
            log = AuditLog.objects.filter(table_id=param_table, entity_id=param_entity).values()
        else:
            return Response({"message":"table and / or entity not found"})
        
        for each in log:
            each['timestamp'] = timestamp_to_strdateformat(str(each['timestamp']), "%d %B %Y")
            each['modified_by'] = User.all_objects.get(pk=each['modified_by']).display_name
        return Response(log)
    
    
# def get_queryset(self):
#     if self.request.method == 'GET':
#         tableid = self.request.GET.get('table_id', None)
#         entityid = self.request.GET.get('entity_id', None)
#         if tableid is not None and entityid is not None:
#             queryset = AuditLog.objects.filter(entity_id=entityid).filter(table_id=tableid)
#         else:
#             queryset = None
#     return queryset
    
