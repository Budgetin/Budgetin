from django.db import models
from api.models import User
class AuditLog(models.Model):
    table = models.CharField(max_length=100)
    action = models.CharField(max_length=50)
    timestamp = models.DateTimeField()
    modified_by = models.BigIntegerField()
    entity_id = models.BigIntegerField()
    serialized_data = models.CharField(max_length=5000)
    
    def format_timestamp(self, format):
        self.timestamp = self.timestamp.strftime(format)
        
    def format_modified_by(self):
        self.modified_by = User.objects.get(pk=self.modified_by).display_name