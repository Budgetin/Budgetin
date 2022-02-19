import pandas
from django.utils.datastructures import MultiValueDictKeyError

from api.exceptions import SheetNotFoundException, FileNotFoundException

def read_file(request):
    try:
        return request.FILES['file'].read()
    except MultiValueDictKeyError:
        raise FileNotFoundException
    

def read_excel(file, sheet_name):
    try:
        df = pandas.read_excel(file, sheet_name=sheet_name)
    except ValueError:
        raise SheetNotFoundException(sheet_name)
    
    return df