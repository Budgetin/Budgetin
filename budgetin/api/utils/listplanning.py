from api.models.project_detail_model import ProjectDetail
from api.models.planning_model import Planning
from api.models.project_model import Project
from api.models.product_model import Product
from api.models.biro_model import Biro
from api.models.project_type_model import ProjectType
import json
from django.forms.models import model_to_dict

def get_all_list_planning():
    listPlanning = ProjectDetail.objects.all().values()
    
    for lp in listPlanning:
        lp['planning'] = model_to_dict(Planning.all_object.get(pk=lp['planning_id']))
        lp['planning'] = model_to_dict(Planning.all_object.get(pk=lp['planning_id']))
        lp['project'] = model_to_dict(Project.objects.get(pk=lp['project_id']))
        lp['project']['product'] = model_to_dict(Product.objects.get(pk=lp['project']['product']))
        lp['project']['biro'] = model_to_dict(Biro.objects.get(ithc_biro=lp['project']['biro_id']))['code']
        lp['project_type'] = model_to_dict(ProjectType.objects.get(pk=lp['project_type_id']))['name']
        lp.pop('planning_id')
        lp.pop('project_id')
        lp['project'].pop('biro_id')
        lp['created_at'] = lp['created_at'].strftime("%d %B %Y")
        lp['updated_at'] = lp['updated_at'].strftime("%d %B %Y")
    return listPlanning