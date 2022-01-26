import json
from rest_framework import viewsets, mixins
from api.models import AuditLog, User, Table
from api.serializers.audit_log_serializer import AuditLogSerializer
from rest_framework.response import Response
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.enum import TableEnum

class AuditLogViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    
    def list(self, request, *args, **kwargs):
        param_table = request.GET.get('table')
        param_entity = request.GET.get('entity')

        if param_table and param_entity:
            log = AuditLog.objects.filter(table_id=self.map_table(param_table), entity_id=param_entity).values()
        else:
            return Response({"message":"table and / or entity not found"})
        
        for each in log:
            each['timestamp'] = timestamp_to_strdateformat(str(each['timestamp']), "%d %B %Y")
            each['modified_by'] = User.all_objects.get(pk=each['modified_by']).display_name
            #Process serialized data to JSON
            data_json = json.loads(each['serialized_data'])
            if data_json['created_at']:
                data_json['created_at'] = timestamp_to_strdateformat(str(data_json['created_at']), "%d %B %Y")
            if data_json['updated_at']:
                data_json['updated_at'] = timestamp_to_strdateformat(str(data_json['updated_at']), "%d %B %Y")
            each['serialized_data'] = data_json
        return Response(log)
    
    def map_table(self, table_name):
        if str.lower(table_name) == "coa":
            return Table.objects.get(name=TableEnum.COA.value).pk
        elif str.lower(table_name) == "biro":
            return Table.objects.get(name=TableEnum.BIRO.value).pk
        elif str.lower(table_name) == "budget":
            return Table.objects.get(name=TableEnum.BUDGET.value).pk
        elif str.lower(table_name) == "monitoring":
            return Table.objects.get(name=TableEnum.MONITORING.value).pk
        elif str.lower(table_name) == "planning":
            return Table.objects.get(name=TableEnum.PLANNING.value).pk
        elif str.lower(table_name) == "product":
            return Table.objects.get(name=TableEnum.PRODUCT.value).pk
        elif str.lower(table_name) == "project":
            return Table.objects.get(name=TableEnum.PROJECT.value).pk
        elif str.lower(table_name) == "projectdetail":
            return Table.objects.get(name=TableEnum.PROJECT_DETAIL.value).pk
        elif str.lower(table_name) == "strategy":
            return Table.objects.get(name=TableEnum.STRATEGY.value).pk
        
        
