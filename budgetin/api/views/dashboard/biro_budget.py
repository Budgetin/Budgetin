from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response

from api.models import Budget
class BiroBudgetView(APIView):
    def get(self, request):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by'
                                                ).filter(project_detail__planning_id = 1).all()
        biro_name = []
        biro_budget = []
        for budget in budgets:
            total = budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4
            biro = budget.project_detail.project.biro.code
            if biro in biro_name:
                biro_budget[biro_name.index(biro)] += total
            else:
                biro_name.append(biro)
                biro_budget.append(total)
        return Response({
            "biro" : biro_name,
            "budget" : biro_budget
        })