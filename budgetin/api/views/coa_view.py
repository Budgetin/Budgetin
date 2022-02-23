from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db import transaction

from api.models import Coa, User
from api.serializers import CoaSerializer, CoaResponseSerializer
from api.permissions import IsAuthenticated, IsAdminOrReadOnly
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum,TableEnum
from api.utils.file import read_file, get_import_template_path, load_file
from api.utils.excel import read_excel, remove_sheet, export_excel, is_empty, export_errors_as_excel
from api.exceptions import ValidationException
from api.views.upload.import_coa import ImportCoa

def is_duplicate_coa_create(name, hyperion_name):
    if Coa.objects.filter(name__iexact=name):
        raise ValidationException('COA ' + name + ' already exists')
    if Coa.objects.filter(hyperion_name__iexact=hyperion_name):
        raise ValidationException('COA with hyperion name ' + hyperion_name + ' already exists')

def is_duplicate_coa(id, name, hyperion_name):
    if Coa.objects.filter(name__iexact=name).exclude(id=id):
        raise ValidationException('COA ' + name + ' already exists')
    if Coa.objects.filter(hyperion_name__iexact=hyperion_name).exclude(id=id):
        raise ValidationException('COA with hyperion name ' + hyperion_name + ' already exists')
    
class CoaViewSet(viewsets.ModelViewSet):
    queryset = Coa.objects.all()
    serializer_class = CoaSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = Coa.objects.select_related('updated_by', 'created_by').all()
        for coa in queryset:
            coa.format_timestamp("%d %B %Y")
            
        serializer = CoaResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        coa =  Coa.objects.select_related('updated_by', 'created_by').get(pk=kwargs['pk'])
        coa.format_timestamp("%d %B %Y")
        
        serializer = CoaResponseSerializer(coa, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['created_by'] = request.custom_user['id']
        request.data['updated_by'] = request.custom_user['id']
        request.data['name'] = request.data['name'].strip()
        request.data['hyperion_name'] = request.data['hyperion_name'].strip()
        is_duplicate_coa_create(request.data['name'],request.data['hyperion_name'])
        coa = super().create(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.CREATE, TableEnum.COA)
        return coa

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        request.data['name'] = request.data['name'].strip()
        request.data['hyperion_name'] = request.data['hyperion_name'].strip()
        is_duplicate_coa(kwargs['pk'],request.data['name'],request.data['hyperion_name'])
        coa = super().update(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.UPDATE, TableEnum.COA)
        return coa

    @transaction.atomic
    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = request.custom_user['id']
        coa = super().destroy(request, *args, **kwargs)
        AuditLog.Save(coa, request, ActionEnum.DELETE, TableEnum.COA)
        return coa
    
    @transaction.atomic
    @action(methods=['post'], detail=False, url_path='import')
    def import_from_excel(self, request):
        return ImportCoa().start(request)
    
    @action(methods=['get'], detail=False, url_path='import/template')
    def download_import_template(self, request):
        file_path = get_import_template_path(TableEnum.COA)
        file = load_file(file_path, 'rb')
        
        return export_excel(file, 'import_template_strategy.xlsx')