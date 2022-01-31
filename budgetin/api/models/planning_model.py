from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel


class Planning(SoftDeleteModel, TimestampModel, UserTrackModel):
    year = models.IntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    notification = models.BooleanField(default=False)
    due_date = models.DateTimeField()

    all_object = models.Manager()
    
    def format_duedate(self, format):
        self.due_date = self.due_date.strftime(format)