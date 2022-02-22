import pandas
import os
from django.utils.datastructures import MultiValueDictKeyError

from api.exceptions import ValidationException, FileNotFoundException

def read_file(request):
    try:
        return request.FILES['file'].read()
    except MultiValueDictKeyError:
        raise ValidationException('File not found.')

def get_import_template_path(table):
    module_dir = os.path.dirname(__file__)
    file_name = 'import_template_' + table.value + '.xlsx'
    file_path = os.path.join(module_dir, "template\\", file_name)
    
    return file_path

def load_file(path, mode):
    try:
        return open(path, mode)
    except:
        raise FileNotFoundException()
    