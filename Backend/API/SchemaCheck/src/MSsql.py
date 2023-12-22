import pyodbc

def connect_to_DB():
    DBconn = pyodbc.connect(driver='{SQL Server}', server='DESKTOP-ALT0UH5', database='SchemaCheck', trusted_connection='yes')
    cursor = DBconn.cursor()
    return cursor
