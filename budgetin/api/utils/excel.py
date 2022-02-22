import pandas

from io import BytesIO
from django.http import HttpResponse
from api.exceptions import  SheetNotFoundException

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

def write_sheet(book, file_path, dataframe, sheet_name):
    writer = pandas.ExcelWriter(file_path, engine = 'openpyxl')
    writer.book = book
    
    if sheet_name in book.sheetnames:
        remove_sheet(book, sheet_name)            
        
    dataframe.to_excel(writer, sheet_name=sheet_name, index=False)
    writer.save()
    writer.close()

def remove_sheet(book, sheet_name):
    std=book.get_sheet_by_name(sheet_name)
    book.remove_sheet(std)

def is_empty(value):
    return pandas.isnull(value)

