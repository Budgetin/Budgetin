from rest_framework import viewsets
from api.models.user_model import User
from api.serializers.user_serializer import UserSerializer
from api.utils.date_format import timestamp_to_strdateformat

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        user = super().list(request, *args, **kwargs)
        for each in user.data:
            #Reformat date
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return user
    
    def retrieve(self, request, *args, **kwargs):
        user = super().retrieve(request, *args, **kwargs)
        user.data['created_at'] = timestamp_to_strdateformat(user.data['created_at'], "%d %B %Y")
        user.data['updated_at'] = timestamp_to_strdateformat(user.data['updated_at'], "%d %B %Y")
        return user