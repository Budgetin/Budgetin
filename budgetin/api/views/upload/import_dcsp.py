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
from api.utils.excel import is_empty, export_errors_as_excel
from django.db.models.base import ObjectDoesNotExist

from api.models import ProjectDetail

def update_db(request, index, data, errors):
    dcsp_id = data['project_id']
    project_detail = get_projectdetail(data['id'], index, errors)
    
    if project_detail != 'project-detail-error':
        if not errors:
            project_detail.dcsp_id = dcsp_id
            project_detail.save()
            AuditLog.Save(ProjectDetailSerializer(project_detail), request, ActionEnum.UPDATE, TableEnum.PROJECT_DETAIL)

def get_projectdetail(pk, index, errors):
    try:
        return ProjectDetail.objects.get(pk=pk)
    except ObjectDoesNotExist:
        errors.append("Row {} - Project Detail with id {} does not exist".format(index, pk))
        return 'project-detail-error'

class ImportDCSP(APIView):
    parser_classes = (MultiPartParser, )
    
    def validate_input(self, index, data):
        project_detail_id = data['id']
        dcsp_id = data['project_id']

        errors = []
        if is_empty(project_detail_id):
            errors.append("Row {} - Id is empty, please refer to the original file (re-download)".format(index))
        if is_empty(dcsp_id):
            errors.append("Row {} - project_id must be filled".format(index))
        return errors


    @transaction.atomic
    def post(self, request, format=None):
        file_obj = request.FILES['file'].read()
        try:
            df = pandas.read_excel(file_obj, sheet_name='DCSP')
        except ValueError:
            raise SheetNotFoundException('DCSP')

        errors = []

        for index, row in df.iterrows():
            line_error = self.validate_input(index, row)
            errors.extend(line_error)
            if not line_error:
                update_db(request, (index+2), row, errors)
        print(errors)
        if errors:
            return export_errors_as_excel(errors)
        return Response(status=204)