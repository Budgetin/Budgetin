from django.http import HttpResponse
from rest_framework.views import APIView
from api.permissions import IsAuthenticated, IsUser
from api.models import Budget, Monitoring
from api.serializers import BudgetResponseSerializer
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
import pandas as pd
from io import BytesIO

from api.views import BudgetViewSet
def get_list(pk, ithc_biro):
    monitoring = Monitoring.objects.select_related('planning').get(pk=pk)
    planning_id = monitoring.planning.id
        
    queryset = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'created_by', 'updated_by')
    queryset = queryset.filter(project_detail__planning__id=planning_id)
    queryset = queryset.filter(project_detail__project__biro__ithc_biro=ithc_biro)

            
    serializer = BudgetResponseSerializer(queryset, many=True)
    return Response(serializer.data)

class ExportMyTask(APIView):
    parser_classes = (MultiPartParser,)
    permission_classes = [IsAuthenticated, IsUser]

    
    def post(self, request, pk=None):
        biro = request.custom_user['ithc_biro']
        data = get_list(pk, biro).data
        print(get_list(pk,request.custom_user['ithc_biro']).data)

        # df = pd.DataFrame(exported_data, columns=collumn)
        # b = BytesIO()
        # writer = pd.ExcelWriter(b, engine='openpyxl')
        # df.to_excel(writer, index=False)
        # writer.save()
        # filename = 'list_planning.xlsx'
        # response = HttpResponse(b.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        # response['Content-Disposition'] = 'attachment; filename=%s' % filename
            
        
        # return response
        return Response({"test":"tist"})