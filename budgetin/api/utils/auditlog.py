import datetime
import json

from django.forms import model_to_dict
from api.models import AuditLog as AL
from api.utils.enum import ActionEnum
class AuditLog():    
    def Save(data, request, action_enum, table_enum):
        
        if data and action_enum != ActionEnum.DELETE:
            try:
                entity_id = data.data['id']
                serialized_data = json.dumps(data.data)
            except AttributeError:
                entity_id = data.id
                serialized_data = json.dumps(model_to_dict(data))
        else:
            entity_id = request.parser_context['kwargs']['pk']
            serialized_data = json.dumps({"message":"entity with id {} deleted from table {}".format(entity_id, table_enum.value)})
            
        AL.objects.create(timestamp=datetime.datetime.now(
            ), modified_by=request.custom_user['id'], entity_id=entity_id, serialized_data=serialized_data, action=action_enum.value, table=table_enum.value)
        # AL.objects.create(timestamp=datetime.datetime.now(
        #     ), modified_by=1, entity_id=entity_id, serialized_data=serialized_data, action=action_enum.value, table=table_enum.value)


#CONTEKAN

# AuditLog.objects.create(timestamp=datetime.datetime.now(
# ), modified_by=request.custom_user['id'], entity_id=coa.data['id'], serialized_data=coa.data, action_id=1, table_id=4)

# AuditLog.objects.create(timestamp=datetime.datetime.now(
# ), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data=coa_update.data, action_id=3, table_id=4)

#AuditLog.Save(coa, request, AuditLog.Delete, AuditLog.Coa)
# AuditLog.objects.create(timestamp=datetime.datetime.now(), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data={
#                         "data": "destroyed"}, action_id=4, table_id=4)