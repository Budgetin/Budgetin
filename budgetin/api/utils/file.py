import pandas
import os
from django.utils.datastructures import MultiValueDictKeyError
from api.utils.enum import TableEnum

from api.exceptions import SheetNotFoundException, ValidationException, FileNotFoundException

def read_file(request):
    try:
        return request.FILES['file'].read()
    except MultiValueDictKeyError:
        raise ValidationException('File not found.')
    

def read_excel(file, sheet_name):
    try:
        df = pandas.read_excel(file, sheet_name=sheet_name)
    except ValueError:
        raise SheetNotFoundException(sheet_name)
    
    return df

def get_import_template(table):
    module_dir = os.path.dirname(__file__)
    file_name = 'import_template_' + table.value + '.xlsx'
    file_path = os.path.join(module_dir, 'template/', file_name)

    try:
        return open(file_path, 'rb')
    except:
        raise FileNotFoundException()