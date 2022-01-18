from tkinter import CASCADE
from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel
from .abstract_model import UserTrackModel


class ProjectDetail(SoftDeleteModel, TimestampModel, UserTrackModel):
    # PlanningId = models.ForeignKey('Planning',on_delete=models.CASCADE)
    # ProjectId = models.ForeignKey('Project',on_delete=models.CASCADE)
    # ProjectTypeId = models.ForeignKey('ProjectType',on_delete=models.CASCADE)
    DcspId = models.CharField(max_length=200)
    Year = models.IntegerField()