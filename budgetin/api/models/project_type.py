from django.db import models

class ProjectType(models.Model):
    name = models.CharField(max_length=200)