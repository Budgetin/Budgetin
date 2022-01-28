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
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user = super().list(request, *args, **kwargs)
        for each in user.data:
            if each['updated_by'] is not None:
                each['updated_by'] = User.objects.get(pk=each['updated_by']).display_name
            else:
                each['updated_by'] = ''
            #Reformat date
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
            
            each['is_active'] = 1 if each['is_active'] else 0 
        return user
    
    def retrieve(self, request, *args, **kwargs):
        user = super().retrieve(request, *args, **kwargs)
        if user.data['updated_by'] is not None:
                user.data['updated_by'] = User.objects.get(pk=user.data['updated_by']).display_name
        else:
            user.data['updated_by'] = ''
        user.data['created_at'] = timestamp_to_strdateformat(user.data['created_at'], "%d %B %Y")
        user.data['updated_at'] = timestamp_to_strdateformat(user.data['updated_at'], "%d %B %Y")

        user.data['is_active'] = 1 if user.data['is_active'] else 0 
        return user

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
        is_duplicate_user(request.data['username'])
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