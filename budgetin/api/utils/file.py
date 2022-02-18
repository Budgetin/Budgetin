import pandas

from api.exceptions import SheetNotFoundException

def read_excel(file, sheet_name):
    try:
        df = pandas.read_excel(file, sheet_name=sheet_name)
    except ValueError:
        raise SheetNotFoundException(sheet_name)
    
    return df