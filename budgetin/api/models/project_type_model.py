from django.db import models

class ProjectType(models.Model):
    name = models.CharField(max_length=200)
    
    @staticmethod
    def name_exists(name):
        return ProjectType.objects.filter(name__iexact=name).count() > 0