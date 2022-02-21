import pandas
import os
from io import BytesIO
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse

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

def export_excel(content, filename):
    response = HttpResponse(content=content)
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    response['Content-Disposition'] = 'attachment; filename="%s"' % filename
    try:
        content.close()
    except:
        pass
    return response

def export_errors_as_excel(errors):
    df = pandas.DataFrame(errors, columns=['errors'])
    b = BytesIO()
    writer = pandas.ExcelWriter(b, engine='openpyxl')
    df.to_excel(writer, index=False)
    writer.save()            
    
    response = export_excel(b.getvalue(), 'validation_error.xlsx')
    response.status_code = 400
    
    return response

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
    
def remove_sheet(book, sheet_name):
    std=book.get_sheet_by_name(sheet_name)
    book.remove_sheet(std)