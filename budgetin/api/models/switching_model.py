from django.db import models

class Switching(models.Model):
    from_minus = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='switching_from', null=True, blank=True)
    to_plus = models.ForeignKey('Budget', on_delete=models.CASCADE, related_name='switching_to', null=True, blank=True)
    nominal = models.BigIntegerField()
    type = models.CharField(max_length=300)