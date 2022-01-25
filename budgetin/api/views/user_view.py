from rest_framework.response import Response
from rest_framework import viewsets
from api.models.user_model import User
from api.serializers.user_serializer import UserSerializer
from api.utils.date_format import timestamp_to_strdateformat
from rest_framework.decorators import action
from api.utils.hit_api import get_imo_d_employee, get_s4, get_employee_info

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user = super().list(request, *args, **kwargs)
        for each in user.data:
            if each['updated_by'] is not None:
                each['updated_by'] = User.objects.filter(id=each['updated_by']).values()[0]['display_name']
            else:
                each['updated_by'] = ''
            #Reformat date
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return user
    
    def retrieve(self, request, *args, **kwargs):
        user = super().retrieve(request, *args, **kwargs)
        if user.data['updated_by'] is not None:
                user.data['updated_by'] = User.objects.filter(id=user.data['updated_by']).values()[0]['display_name']
        else:
            user.data['updated_by'] = ''
        user.data['created_at'] = timestamp_to_strdateformat(user.data['created_at'], "%d %B %Y")
        user.data['updated_at'] = timestamp_to_strdateformat(user.data['updated_at'], "%d %B %Y")
        return user

    def create(self, request, *args, **kwargs):
        employee_info = get_employee_info(request.data['username'])
        request.data['employee_id'] = employee_info['employee_id']
        request.data['display_name'] = employee_info['display_name']
        return super().create(request, *args, **kwargs)

    @action(detail=False, methods=['get'])
    def imo(self, request, pk=None):
        imod = get_imo_d_employee()
        # s4 = get_s4()
        return Response(imod)