from django.db import models

class AuditLog(models.Model):
    table_id = models.ForeignKey('Table',on_delete=models.CASCADE)
    action_id = models.ForeignKey('Action', on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    modified_by = models.BigIntegerField()
    serialized_data = models.CharField(max_length=5000)