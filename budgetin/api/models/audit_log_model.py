from django.db import models

class AuditLog(models.Model):
    table = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    modified_by = models.BigIntegerField()
    entity_id = models.BigIntegerField()
    serialized_data = models.CharField(max_length=5000)