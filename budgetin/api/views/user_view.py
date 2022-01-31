from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action

from api.models import User
from api.serializers import UserSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.hit_api import get_imo_d_employee, get_ithc_employee_info
from api.exceptions.validation_exception import ValidationException

def is_duplicate_user(username):
    if User.objects.filter(username=username):
        raise ValidationException

def is_duplicate_user_update(id, username):
    if User.objects.filter(username=username).exclude(pk=id):
        raise ValidationException
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        for user in queryset:
            user.format_timestamp("%d %B %Y")
            user.format_created_updated_by()
        
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        user.format_timestamp("%d %B %Y")
        user.format_created_updated_by()
        
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        is_duplicate_user(request.data['username'])
        employee_info = get_ithc_employee_info(request.data['username'])
        request.data['employee_id'] = employee_info['employee_id']
        request.data['display_name'] = employee_info['display_name']
        request.data['created_by'] = 1
        user = super().create(request, *args, **kwargs)
        AuditLog.Save(user, request, ActionEnum.CREATE, TableEnum.USER)
        return user

    def update(self, request, *args, **kwargs):
        is_duplicate_user_update(kwargs['pk'], request.data['username'])
        user = super().update(request, *args, **kwargs)
        AuditLog.Save(user, request, ActionEnum.UPDATE, TableEnum.USER)
        return user
    
    def destroy(self, request, *args, **kwargs):
        return Response({
            'message': 'User cannot be deleted'
        })

    @action(detail=False, methods=['get'])
    def imo(self, request, pk=None):
        imod = get_imo_d_employee()
        return Response(imod)