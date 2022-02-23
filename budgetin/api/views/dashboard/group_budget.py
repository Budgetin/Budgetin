from datetime import datetime
from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Budget, Biro, Planning
from django.db.models.base import ObjectDoesNotExist
from api.exceptions import NotFoundException
class GroupBudgetView(APIView):
    def get(self, request):
        current_year = datetime.now().year
        try:
            planning = Planning.objects.get(year=current_year)
        except ObjectDoesNotExist:
            raise NotFoundException("Planning with year {}".format(current_year))
        try:
            budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project__biro'
                                                ).filter(project_detail__planning = planning).all()  
        except ObjectDoesNotExist:
            raise NotFoundException("Budget with planning year {}".format(current_year))      
        res = []
        added_group=[]
        for budget in budgets:
            total = budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4
            group = budget.project_detail.project.biro.group_code

            if group not in added_group:
                added_group.append(group)
                res.append({"Group": group, "Budget":total, "Realisasi":0})
            else:
                res[added_group.index(group)]["Budget"]+=total
                #DEBT ADD REALISASI
        return Response(res)