from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
from rest_framework.parsers import MultiPartParser
import io
from api.utils.read_excel import read_excel

class ImportExcelView(APIView):
    parser_classes = (MultiPartParser,)
    
    def post(self, request, format=None):
        file_obj = request.FILES['file'].read()
        file_data = request.data
        read_excel(file_obj)
        
        return Response(status=204)