from django.db import models
from django.apps import apps

class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def format_timestamp(self, format):
        self.created_at = self.created_at.strftime(format)
        self.updated_at = self.updated_at.strftime(format)

    class Meta:
        abstract = True


class UserTrackModel(models.Model):
    created_by = models.BigIntegerField(blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)

    def format_created_updated_by(self):
        User = apps.get_model('api', 'User')
        if self.created_by:     
            self.created_by = User.objects.get(pk=self.created_by).display_name
        else:
            self.created_by = ''
                
        if self.updated_by:
            self.updated_by = User.objects.get(pk=self.updated_by).display_name
        else:
            self.updated_by = ''
    class Meta:
        abstract = True
