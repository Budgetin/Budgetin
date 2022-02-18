from django.utils import timezone
import json

from django.forms import model_to_dict
from api.models import AuditLog as AL
from api.utils.enum import ActionEnum
class AuditLog():    
    def Save(data, request, action_enum, table_enum):
        
        if data and action_enum != ActionEnum.DELETE:
            entity_id = data.data['id']
            serialized_data = json.dumps(data.data)
        else:
            entity_id = request.parser_context['kwargs']['pk']
            serialized_data = json.dumps({"message":"entity with id {} deleted from table {}".format(entity_id, table_enum.value)})
            
        AL.objects.create(
            timestamp=timezone.now(), 
            modified_by=request.custom_user['id'], 
            entity_id=entity_id, 
            serialized_data=serialized_data, 
            action=action_enum.value, 
            table=table_enum.value
        )
