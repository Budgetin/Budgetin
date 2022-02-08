from django_filters import rest_framework as filters

from api.models import Project

class ProjectFilter(filters.FilterSet):
    project_name = filters.CharFilter()
    
    class Meta:
        model = Project
        fields = {
            'project_name': ['exact', 'contains']
        }
