from django.forms import model_to_dict
from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Project, Biro, Product, ProjectDetail, Planning, ProjectType, Budget, Coa, User

class CreateListPlanning(APIView):

    def post(self, request):
        
        # Project
        if 'project_id' not in request.data:
            project = Project.objects.create(
                project_name = request.data['project_name'],
                project_description = request.data['project_description'],
                biro_id = request.data['biro'],
                start_year = request.data['start_year'],
                end_year = request.data['end_year'],
                total_investment_value = request.data['total_investment_value'],
                product_id = request.data['product'],
                is_tech = request.data['is_tech']
            )
            project.generate_itfamid()
        else:
            project = Project.objects.get(pk=request.data['project_id'])
            
        # Project Detail
        project_detail, _ = ProjectDetail.objects.update_or_create(planning_id=request.data['planning'], project=project, defaults={
            'project_type_id': request.data['project_type'],
            'dcsp_id': request.data['dcsp_id'] if 'dcsp_id' in request.data else None
        })
        
        # Budget
        if len(request.data['budget']) == 0:
            Budget.objects.create(project_detail=project_detail)
        for budget in request.data['budget']:
            Budget.objects.create(
                project_detail = project_detail,
                coa_id = budget['coa'],
                expense_type = budget['expense_type'],
                planning_q1 = budget['planning_q1'],
                planning_q2 = budget['planning_q2'],
                planning_q3 = budget['planning_q3'],
                planning_q4 = budget['planning_q4'],
            )
            
        return Response(model_to_dict(project))