from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from django.db import transaction

from api.permissions import IsAuthenticated, IsAdmin
from api.models import User
from api.serializers import UserSerializer, UserResponseSerializer
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum
from api.utils.date_format import timestamp_to_strdateformat
from api.utils.hit_api import get_imo_d_employee, get_ithc_employee_info
from api.exceptions.validation_exception import ValidationException

def is_duplicate_user(username):
    if User.objects.filter(username__iexact=username):
        raise ValidationException('User ' + username + ' already exists')

def is_duplicate_user_update(id, username):
    if User.objects.filter(username__iexact=username).exclude(pk=id):
        raise ValidationException('User ' + username + ' already exists')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]
    
    def list(self, request, *args, **kwargs):
        queryset = User.objects.all()
        for user in queryset:
            user.format_timestamp("%d %B %Y")
        
        serializer = UserResponseSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        user = User.objects.select_related('created_by','updated_by').get(pk=kwargs['pk'])
        user.format_timestamp("%d %B %Y")
        
        serializer = UserResponseSerializer(user, many=False)
        return Response(serializer.data)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        request.data['username'] = request.data['username'].strip()
        is_duplicate_user(request.data['username'])
        employee_info = get_ithc_employee_info(request.data['username'])
        request.data['employee_id'] = employee_info['employee_id']
        request.data['display_name'] = employee_info['display_name']
        request.data['updated_by'] = request.custom_user['id']
        request.data['created_by'] = request.custom_user['id']
        user = super().create(request, *args, **kwargs)
        AuditLog.Save(user, request, ActionEnum.CREATE, TableEnum.USER)
        return user

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        request.data['username'] = request.data['username'].strip()
        is_duplicate_user_update(kwargs['pk'], request.data['username'])
        request.data['updated_by'] = request.custom_user['id']
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
        users =  User.objects.all().values()
        arr_user = []
        for user in users:
            arr_user.append(user['username'])
            
        for idx, imo in enumerate(imod):
            if imo['username'] in arr_user:
                imod.pop(idx)
        return Response(imod)