from rest_framework import viewsets
from api.models.pic_budget_model import PicBudget
from api.serializers.pic_budget_serializer import PicBudgetSerializer
from api.utils.date_format import timestamp_to_strdateformat

#For Audit Logging
from api.utils.auditlog import AuditLog
from api.utils.enum import ActionEnum, TableEnum

class PicBudgetViewSet(viewsets.ModelViewSet):
    queryset = PicBudget.objects.all()
    serializer_class = PicBudgetSerializer

    def list(self, request, *args, **kwargs):
        pic_budget = super().list(request, *args, **kwargs)
        for each in pic_budget.data:
            each['created_at'] = timestamp_to_strdateformat(each['created_at'], "%d %B %Y")
            each['updated_at'] = timestamp_to_strdateformat(each['updated_at'], "%d %B %Y")
        return pic_budget
    
    def retrieve(self, request, *args, **kwargs):
        pic_budget = super().retrieve(request, *args, **kwargs)
        pic_budget.data['created_at'] = timestamp_to_strdateformat(pic_budget.data['created_at'], "%d %B %Y")
        pic_budget.data['updated_at'] = timestamp_to_strdateformat(pic_budget.data['updated_at'], "%d %B %Y")
        return pic_budget

    def create(self, request, *args, **kwargs):
        #request.data['created_by'] = request.custom_user['id']
        request.data['created_by'] = 899
        pic_budget = super().create(request, *args, **kwargs)
        AuditLog.Save(pic_budget, request, ActionEnum.CREATE, TableEnum.PIC_BUDGET)
        return pic_budget

    def update(self, request, *args, **kwargs):
        request.data['updated_by'] = 899
        pic_budget = super().update(request, *args, **kwargs)
        AuditLog.Save(pic_budget, request, ActionEnum.UPDATE, TableEnum.PIC_BUDGET)
        return pic_budget

    def destroy(self, request, *args, **kwargs):
        request.data['updated_by'] = 899                                 
        pic_budget = super().destroy(request, *args, **kwargs)
        AuditLog.Save(pic_budget, request, ActionEnum.DELETE, TableEnum.PIC_BUDGET)
        return pic_budget
