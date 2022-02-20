import pandas as pd

from django.http import HttpResponse
from io import BytesIO

from api.utils.file import export_excel

def export_budget_as_excel(budgets):
    data_temp = []
    exported_data = []
    column = ['Id', 'Id ITFAM', 'Project Id', 'Project Name', 'Project Description', 'Tech / Non Tech',
         'Product Id', 'RCC', 'Project Type', 'Biro', 'Start Year', 'End Year', 'Strategy', 'Is Active', 'Last Updated By', 
         'Total Investment', 'Is Budget', 'COA', 'Capex/Opex', 'Budget This Year', 'Q1', 'Q2', 'Q3', 'Q4']
    
    for budget in budgets:
        project_detail = budget.project_detail
        project = project_detail.project
        project_type = project_detail.project_type
        product = project.product
        biro = project.biro
        strategy = product.strategy
        updated_by = budget.updated_by
        coa = budget.coa
        
        data_temp.append(project_detail.id) 
        data_temp.append(project_detail.project.itfam_id)   
        data_temp.append(project_detail.dcsp_id)
        data_temp.append(project.project_name)
        data_temp.append(project.project_description)
        data_temp.append('Tech' if project.is_tech else 'Non Tech')
        data_temp.append(product.product_code)
        data_temp.append(biro.rcc if biro.rcc else '')
        data_temp.append(project_type.name)
        data_temp.append(biro.code)
        data_temp.append(project.start_year)
        data_temp.append(project.end_year)
        data_temp.append(strategy.name if strategy else '')
        data_temp.append('Active' if budget.is_active else 'Inactive')
        if budget.updated_by:
            data_temp.append(updated_by.display_name)
        else:
            data_temp.append('')
        data_temp.append(project.total_investment_value)
        #isBudget
        if budget.coa:
            data_temp.append('Budget')
            data_temp.append(coa.name)
        else:
            data_temp.append('Non Budget')
            data_temp.append('')
        data_temp.append(budget.expense_type)
        #SUM Budget for this year budget
        budget_this_year = budget.planning_q1 + budget.planning_q2 + budget.planning_q3 + budget.planning_q4
        data_temp.append(budget_this_year)
        data_temp.append(budget.planning_q1)
        data_temp.append(budget.planning_q2)
        data_temp.append(budget.planning_q3)
        data_temp.append(budget.planning_q4)
        #Append and clear temp
        exported_data.append(data_temp)
        data_temp = []

    df = pd.DataFrame(exported_data, columns=column)
    b = BytesIO()
    writer = pd.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()
    
    return export_excel(b.getvalue(), 'budget.xlsx')