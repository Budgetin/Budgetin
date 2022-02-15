from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Budget
from api.permissions import IsAuthenticated, IsUser
from api.serializers import BudgetResponseSerializer

class MyBudgetViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsUser]
     
    def list(self, request):
        print(request.custom_user)
        user_ithc_biro = request.custom_user['ithc_biro']

        queryset = Budget.objects.select_related('coa', 'project_detail', 'project_detail__planning', 
                                                'project_detail__project', 'project_detail__project_type', 
                                                'project_detail__project__biro', 'project_detail__project__product', 
                                                'project_detail__project__product__strategy', 'updated_by', 'created_by').all()            
        queryset = queryset.filter(biro__ithc_biro=user_ithc_biro)
        
        for budget in queryset:
            budget.format_timestamp("%d %B %Y")
            
            
        serializer = BudgetResponseSerializer(queryset, many=True)
        return Response(serializer.data)