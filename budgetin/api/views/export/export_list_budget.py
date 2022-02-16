from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser

from django.forms import model_to_dict
from api.models import Budget
from api.utils.export_budget import export_as_excel

class ExportListBudget(APIView):
    parser_classes = (MultiPartParser,)
    
    def post(self, request, format=None):
        budgets = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                        'project_detail__project', 'project_detail__project_type', 
                                        'project_detail__project__biro', 'project_detail__project__product', 
                                        'project_detail__project__product__strategy', 'updated_by').all()

        return export_as_excel(budgets)