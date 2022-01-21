from tkinter import CASCADE
from django.db import models
from django_softdelete.models import SoftDeleteModel
from .abstract_model import TimestampModel
from .abstract_model import UserTrackModel


class ProjectDetail(SoftDeleteModel, TimestampModel, UserTrackModel):
    planning = models.ForeignKey('Planning',on_delete=models.CASCADE)
    project = models.ForeignKey('Project',on_delete=models.CASCADE)
    project_type = models.ForeignKey('ProjectType',on_delete=models.CASCADE)
    dcsp_id = models.CharField(max_length=200)
    year = models.IntegerField()