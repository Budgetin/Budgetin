from api.models.biro_model import Biro
from api.utils.hit_api import get_all_biro

def create_update_all_biro(biros):
    for biro in biros:
        Biro.objects.update_or_create(
                ithc_biro=biro['id'],
                defaults={'code': biro['code'], 'name': biro['name']}
            )