import datetime
import json
from api.models.audit_log_model import AuditLog as AL
from api.models.action_model import Action
from api.models.table_model import Table

from api.utils.enum import ActionEnum
class AuditLog():
    #Action Name
    Create = "Create"
    Read = "Read"
    Update = "Update"
    Delete = "Delete"
    
    #Table Name
    AuditLog = "Audit Log"
    Biro = "Biro"
    Budget = "Budget"
    Coa = "Coa"
    Monitoring = "Monitoring"
    PicBudget = "PicBudget"
    Planning = "Planning"
    Product = "Product"
    Project = "Project"
    ProjectDetail = "Project Detail"
    
    def Save(data, request, action_enum, entity_enum):
        actionid = Action.objects.filter(name=action_enum.value).values()[0]['id']
        tableid = Table.objects.filter(name=entity_enum.value).values()[0]['id']
        
        if data and action_enum != ActionEnum.DELETE:
            entity_id = data.data['id']
            serialized_data = json.dumps(data.data)
        else:
            entity_id = request.parser_context['kwargs']['pk']
            serialized_data = {"data":"deleted"}
            
        # AL.objects.create(timestamp=datetime.datetime.now(
        #     ), modified_by=request.custom_user['id'], entity_id=entity_id, serialized_data=serialized_data, action_id=actionid, table_id=tableid)
        AL.objects.create(timestamp=datetime.datetime.now(
            ), modified_by=1, entity_id=entity_id, serialized_data=serialized_data, action_id=actionid, table_id=tableid)


#CONTEKAN

# AuditLog.objects.create(timestamp=datetime.datetime.now(
# ), modified_by=request.custom_user['id'], entity_id=coa.data['id'], serialized_data=coa.data, action_id=1, table_id=4)

# AuditLog.objects.create(timestamp=datetime.datetime.now(
# ), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data=coa_update.data, action_id=3, table_id=4)

#AuditLog.Save(coa, request, AuditLog.Delete, AuditLog.Coa)
# AuditLog.objects.create(timestamp=datetime.datetime.now(), modified_by=request.custom_user['id'], entity_id=kwargs['pk'], serialized_data={
#                         "data": "destroyed"}, action_id=4, table_id=4)