from rest_framework.views import APIView
from rest_framework.response import Response
from api.models import Project, Biro, Product, ProjectDetail, Planning, ProjectType, Budget, Coa

class CreateListPlanning(APIView):

    def post(self, request):
        data = request.data
        #DEBT

        # Project Part #
        #DEBT ITFAM ID AUTO GENERATE, USING YEAR + PK,
        # PERTAMA INSERT DULU KE DB
        # AMBIL IDNYA BARU BIKIN ITFAM ID
        # UPDATE DI DB ITFAM YG SUDAH TERISI
        project_data = {
            'itfam_id' : data['itfam_id'],
            'project_name' : data['project_name'],
            'project_description' : data['project_description'],
            'biro' : Biro.all_object.get(pk=data['biro']),
            'start_year': data['start_year'],
            'end_year' : data['end_year'],
            'total_investment_value' : data['total_investment_value'],
            'product' : Product.all_object.get(pk=data['product']),
            'is_tech' : data['is_tech'],
        #DEBT
            'created_by' : 1
        }
        project_data.pop('itfam_id')
        project, _ = Project.objects.update_or_create(itfam_id = data['itfam_id'], defaults = project_data)

        # Project Detail Part #
        parsed_project_detail = ProjectDetail(
            planning = Planning.all_object.get(pk=data['planning']),
            # project = parsed_project,
            project = project,
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