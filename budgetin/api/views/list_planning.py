from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Project, Biro, Product, ProjectDetail, Planning, ProjectType, Budget, Coa

class CreateListPlanning(APIView):

    def post(self, request):
        data = request.data
        #DEBT

        # Project Part #
        parsed_project = Project(
            itfam_id = data['itfam_id'],
            project_name = data['project_name'],
            project_description = data['project_description'],
            biro = Biro.all_object.get(pk=data['biro']),
            start_year = data['start_year'],
            end_year = data['end_year'],
            total_investment_value = data['total_investment_value'],
            product = Product.all_object.get(pk=data['product']),
            is_tech = data['is_tech'],
        #DEBT
            created_by = 1
        )
        #if the project has the same itfam_id, do an update instead of insert
        dup_project = Project.objects.get(itfam_id = data['itfam_id'])
        if dup_project:
            parsed_project.id = dup_project.pk
            parsed_project.created_at = dup_project.created_at
        parsed_project.save()

        # Project Detail Part #
        parsed_project_detail = ProjectDetail(
            planning = Planning.all_object.get(pk=data['planning']),
            project = parsed_project,
            project_type = ProjectType.objects.get(pk=data['project_type']),
            dcsp_id = data['dcsp_id'],
        #DEBT
            created_by = 1
        )
        parsed_project_detail.save()

        # Budget Part #
        for budget in data['budget']:
            parsed_budget = Budget(
                project_detail = parsed_project_detail,
                coa = Coa.objects.get(pk=budget['coa']),
                expense_type = budget['expense_type'],
                planning_q1 = budget['planning_q1'],
                planning_q2 = budget['planning_q2'],
                planning_q3 = budget['planning_q3'],
                planning_q4 = budget['planning_q4'],
            #DEBT
                created_by = 1
            )
            parsed_budget.save()

        return Response({"message":"List Planning Saved"},status=201)