import pandas

def read_excel(file):
    pd = pandas.read_excel(file)
    print(pd.head())