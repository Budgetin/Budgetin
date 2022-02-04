from rest_framework.views import APIView
from rest_framework.response import Response


class TestView(APIView):
    def get(self, request):
        #print something
        return Response({
            "itfam_id" : "ID",
            "project_name" : "PN",
            "project_description" : "PD",
            "biro" : 1,
            "start_year" : 2022,
            "end_year" : 2023,
            "total_investment_value" : 1000000,
            "product" : 1,
            "is_tech" : 1,
            "planning" : 1,
            "project_type" : 1,
            "dcsp_id" : "DCSPID",
            "budget":[
                {
                    "coa" : 1,
                    "expense_type" : "OPEX",
                    "planning_q1" : 100000,
                    "planning_q2" : 100000,
                    "planning_q3" : 100000,
                    "planning_q4" : 100000
                },
                {
                    "coa" : 2,
                    "expense_type" : "CAPEX",
                    "planning_q2" : 200000,
                    "planning_q1" : 200000,
                    "planning_q3" : 200000,
                    "planning_q4" : 200000
                }
            ]
        })

    def post(self, request):
        print(request.data)
        return Response({'status': 'ok'})