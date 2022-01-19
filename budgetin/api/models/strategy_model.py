from django.db import models

class Strategy(models.Model):
    name = models.CharField(max_length=200)
