from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
import pandas as pd
from io import BytesIO

from api.views import ProjectViewSet
class ExportListProject(APIView):
    parser_classes = (MultiPartParser,)
    
    def get(self, request, format=None):
        exported_data = []
        collumn = ['ID ITFAM', 'Project Name', 'Project Description', 'RCC', 'Biro', 'Product Code', 'Start Year', 'End Year']
        datas = ProjectViewSet.list_for_export().data
        #Fill the data
        data_temp = []
        for data in datas:
            data_temp.append(data['itfam_id'])
            data_temp.append(data['project_name'])
            data_temp.append(data['project_description'])
            data_temp.append(data['biro']['rcc'])
            data_temp.append(data['biro']['code'])
            data_temp.append(data['product']['product_code'])
            data_temp.append(data['start_year'])
            data_temp.append(data['end_year'])

            #Append and clear temp
            exported_data.append(data_temp)
            data_temp = []

        df = pd.DataFrame(exported_data, columns=collumn)
        b = BytesIO()
        writer = pd.ExcelWriter(b, engine='openpyxl')
        df.to_excel(writer, index=False)
        writer.save()
        filename = 'list_project.xlsx'
        response = HttpResponse(b.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
            
        
        return response