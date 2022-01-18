from rest_framework import viewsets 
from api.models.table_model import Table
from api.serializers.table_serializer import TableSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer