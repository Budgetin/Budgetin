from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import parser_classes, api_view
from rest_framework.parsers import MultiPartParser
import pandas as pd
from io import BytesIO

from api.views import BudgetViewSet
from rest_framework.decorators import action
class ExportExcelView(APIView):
    parser_classes = (MultiPartParser,)
    
    def get(self, request, format=None):
        exported_data = []
        collumn = ['ID ITFAM', 'Project ID', 'Project Name', 'Project Description', 'Tech / Non Tech',
         'Product ID', 'RCC', 'Project Type', 'Biro', 'Start Year', 'End Year', 'Strategy', 
         'Created By', 'Updated At', 'Total Investment', 'Is Budget', 'COA', 'Capex/Opex', 'Budget This Year', 'Q1', 'Q2', 'Q3', 'Q4']
        datas = BudgetViewSet.list_for_export().data
        #Fill the data
        data_temp = []
        for data in datas:
            data_temp.append(data['project_detail']['project']['itfam_id'])
            data_temp.append(data['project_detail']['dcsp_id'])
            data_temp.append(data['project_detail']['project']['project_name'])
            data_temp.append(data['project_detail']['project']['project_description'])
            data_temp.append(data['project_detail']['project']['is_tech'])
            data_temp.append(data['project_detail']['project']['product']['product_code'])
            data_temp.append(data['project_detail']['project']['biro']['rcc'] if data['project_detail']['project']['biro']['rcc'] else '')
            data_temp.append(data['project_detail']['project_type'])
            data_temp.append(data['project_detail']['project']['biro']['code'])
            data_temp.append(data['project_detail']['project']['start_year'])
            data_temp.append(data['project_detail']['project']['end_year'])
            data_temp.append(data['project_detail']['project']['total_investment_value'])
            data_temp.append(data['project_detail']['project']['product']['strategy'])
            data_temp.append(data['created_by'])
            data_temp.append(data['updated_at'])
            data_temp.append(1)
            #SUM Budget for this year budget
            # if data['budget']:
            data_temp.append(data['coa'])
            data_temp.append(data['expense_type'])
            budget_this_year = data['planning_q1'] + data['planning_q2'] + data['planning_q3'] + data['planning_q4']
            data_temp.append(budget_this_year)
            data_temp.append(data['planning_q1'])
            data_temp.append(data['planning_q2'])
            data_temp.append(data['planning_q3'])
            data_temp.append(data['planning_q4'])

            #Append and clear temp
            exported_data.append(data_temp)
            data_temp = []

        df = pd.DataFrame(exported_data, columns=collumn)
        b = BytesIO()
        writer = pd.ExcelWriter(b, engine='openpyxl')
        df.to_excel(writer, index=False)
        writer.save()
        filename = 'list_planning.xlsx'
        response = HttpResponse(b.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
            
        
        return response