from api.models import Planning

def filter(param, filter):
    if param == "planning":
        return Planning.all_object.filter(param=filter)