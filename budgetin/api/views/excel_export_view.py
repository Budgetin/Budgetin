from wsgiref.util import FileWrapper
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
import pandas as pd
from io import BytesIO

class ExportExcelView(APIView):
    parser_classes = (MultiPartParser,)
    
    def get(self, request, format=None):
        #Get Excel di panda -> data frame
        df = pd.DataFrame([[11, 21, 31], [12, 22, 32], [31, 32, 33]],
                  index=['one', 'two', 'three'], columns=['a', 'b', 'c'])

        b = BytesIO()
        writer = pd.ExcelWriter(b, engine='openpyxl')
        df.to_excel(writer)
        writer.save()
        filename = 'filename.xlsx'
        response = HttpResponse(b.getvalue(),content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=%s' % filename
        
        return response