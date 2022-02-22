from django.db import models
from django_softdelete.models import SoftDeleteModel

from api.models.abstract_model import TimestampModel, UserTrackModel


class ProjectDetail(SoftDeleteModel, TimestampModel, UserTrackModel):
    planning = models.ForeignKey('Planning',on_delete=models.CASCADE)
    project = models.ForeignKey('Project',on_delete=models.CASCADE, related_name='project_detail')
    project_type = models.ForeignKey('ProjectType',on_delete=models.CASCADE)
    dcsp_id = models.CharField(max_length=200, blank=True, null=True)
    
    def equal(self, project_detail):
        return self.dcsp_id == project_detail.dcsp_id