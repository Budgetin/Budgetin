import json

from rest_framework import viewsets, mixins
from rest_framework.response import Response

from api.models import AuditLog, User, Strategy
from api.serializers import AuditLogSerializer
from django.forms.models import model_to_dict
from api.utils.date_format import timestamp_to_strdateformat

class AuditLogViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    
    def list(self, request, *args, **kwargs):
        param_table = request.GET.get('table')
        param_entity = request.GET.get('entity')

        if param_table and param_entity:
            log = AuditLog.objects.filter(table=param_table, entity_id=param_entity).values()
        else:
            return Response({"message":"table and / or entity not found"})
        for each in log:
            each['timestamp'] = timestamp_to_strdateformat(str(each['timestamp']), "%d %B %Y")
            each['modified_by'] = User.all_objects.get(pk=each['modified_by']).display_name
            data_as_json = json.loads(each['serialized_data'])
            if each['action'] != "Delete":
                data_as_json['is_deleted'] = 1 if data_as_json['is_deleted']==True else 0
                if 'is_capex' in data_as_json:
                    data_as_json['is_capex'] = 1 if data_as_json['is_capex']==True else 0
                if 'strategy' in data_as_json:
                    data_as_json['strategy'] = model_to_dict(Strategy.all_objects.get(pk=data_as_json['strategy']))
                data_as_json['created_at'] = timestamp_to_strdateformat(str(data_as_json['created_at']), "%d %B %Y")
                data_as_json['created_by'] = User.all_objects.get(pk=data_as_json['created_by']).display_name
                data_as_json['updated_at'] = timestamp_to_strdateformat(str(data_as_json['updated_at']), "%d %B %Y")
                if data_as_json['updated_by']:
                    data_as_json['updated_by'] = User.all_objects.get(pk=data_as_json['updated_by']).display_name
            each['serialized_data'] = data_as_json
        return Response(log)
        
