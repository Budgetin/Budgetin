import datetime
from api.models.audit_log_model import AuditLog as AL
from api.models.action_model import Action
from api.models.table_model import Table

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
    Planning = "Planning"
    Product = "Product"
    Project = "Project"
    ProjectDetail = "Project Detail"
    
    def Save(data, request, action_name, entity_name):
        action_id = Action.objects.filter(name=action_name).values()[0]['id']
        table_id = Table.objects.filter(name=entity_name).values()[0]['id']
        
        if data and action_name != AuditLog.Delete:
            entity_id = data.data['id']
            serialized_data = data.data
        else:
            entity_id = request.parser_context['kwargs']['pk']
            serialized_data = {}
            
        
        AL.objects.create(timestamp=datetime.datetime.now(
            ), modified_by=request.custom_user['id'], entity_id=entity_id, serialized_data=serialized_data, action_id_id=action_id, table_id_id=table_id)

        
