from django.forms import model_to_dict
import pandas

from django.db import transaction
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from api.exceptions import SheetNotFoundException, NotFoundException
from api.utils.enum import ActionEnum, TableEnum
from api.utils.auditlog import AuditLog
from api.serializers import ProjectDetailSerializer
from django.db.models.base import ObjectDoesNotExist

from api.models import ProjectDetail

def update_db(request, index, data):
    dcsp_id = data['Project Id']
    project_detail = get_projectdetail(data['Id'], index)
    project_detail.update(dcsp_id = dcsp_id)
    AuditLog.Save(ProjectDetailSerializer(project_detail), request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)

def get_projectdetail(pk, index):
    try:
        return ProjectDetail.objects.get(pk=pk)
    except ObjectDoesNotExist:
        raise NotFoundException("Project Detail with Id "+str(pk)+" on line "+str(index))

class ImportDCSP(APIView):
    parser_classes = (MultiPartParser, )
    
    @transaction.atomic
    def post(self, request, format=None):
        file_obj = request.FILES['file'].read()
        try:
            df = pandas.read_excel(file_obj, sheet_name='Realisasi')
        except ValueError:
            raise SheetNotFoundException('Realisasi')
        
        for index, row in df.iterrows():
            update_db(request, (index+2), row)
            
        return Response(status=204)