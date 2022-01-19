from django.db import models

class MonitoringStatus(models.Model):
    name = models.CharField(max_length=200)