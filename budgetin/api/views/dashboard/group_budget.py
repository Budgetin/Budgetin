from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Budget, Biro

def merge_two_dict(x,y):
    z = x.copy
    z.update(y)
    return z
class GroupBudgetView(APIView):
    def get(self, request):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by'
                                                ).filter(project_detail__planning_id = 1).all()
        groups = Biro.objects.distinct('group_code').all()
        print(groups)
        res = []
        tahun_added = []
        for budget in budgets:
            total = budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4
            group = budget.project_detail.project.biro.group_code
            tahun = budget.project_detail.planning.year
            if tahun not in tahun_added:
                tahun_obj = {}
                tahun_added.append(tahun)
                for group in groups:
                    if 'GTI' in group.group_code or 'SKES' in group.group_code:
                        continue
                    tahun_obj = tahun_obj | {group.group_code:0}
                res.append({"Tahun" : tahun, "Group" : tahun_obj})
            else:
                res[tahun_added.index(tahun)]['Group'][group] += total
        return Response(res)