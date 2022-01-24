
import json
from api.models.strategy_model import Strategy


def include(param, paramid):
    if param == "strategy":
        return Strategy.objects.filter(id=paramid).values()[0]
