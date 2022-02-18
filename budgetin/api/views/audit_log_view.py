import json

from django.forms.models import model_to_dict
from rest_framework import viewsets, mixins
from rest_framework.response import Response

from api.models import AuditLog, User, Strategy, Product, Biro, Coa
from api.serializers import AuditLogSerializer
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.enum import ActionEnum

class AuditLogViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    
    def list(self, request, *args, **kwargs):
        table = request.query_params['table']
        entity_id = request.query_params['entity']
        
        if not table or not entity_id:
            return Response({"message": "table and/or entity not found"})
        
        logs = AuditLog.objects.filter(table=table, entity_id=entity_id)
        for log in logs:
            log.format_timestamp('%d %B %Y')
            log.format_modified_by()
            serialized_data = json.loads(log.serialized_data)
            if log.action != ActionEnum.DELETE.value:
                serialized_data['is_deleted'] = 1 if serialized_data['is_deleted'] else 0
                if 'is_capex' in serialized_data:
                    serialized_data['is_capex'] = 1 if serialized_data['is_capex'] else 0
                if 'strategy' in serialized_data:
                    serialized_data['strategy'] = model_to_dict(Strategy.all_objects.get(pk=serialized_data['strategy']))
                if 'created_by' in serialized_data and serialized_data['created_by']:
                    serialized_data['created_by'] = User.objects.get(pk=serialized_data['created_by']).display_name
                if 'updated_by' in serialized_data and serialized_data['updated_by']:
                    serialized_data['updated_by'] = User.objects.get(pk=serialized_data['updated_by']).display_name
                if 'product' in serialized_data and serialized_data['product']:
                    serialized_data['product'] = Product.objects.get(pk=serialized_data['product']).product_name
                if 'biro' in serialized_data and serialized_data['biro']:
                    serialized_data['biro'] = Biro.objects.get(pk=serialized_data['biro']).code
                if 'coa' in serialized_data and serialized_data['coa']:
                    serialized_data['coa'] = Coa.objects.get(pk=serialized_data['coa']).name

                serialized_data['created_at'] = timestamp_to_strdateformat(str(serialized_data['created_at']), "%d %B %Y")
                serialized_data['updated_at'] = timestamp_to_strdateformat(str(serialized_data['updated_at']), "%d %B %Y")
                
            log.serialized_data = serialized_data
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data)
        
