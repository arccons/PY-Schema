import pandas
import numpy
import SchemaCheck.src.MSsql as MSsql

def getFileSubject(subject):
    cursor = MSsql.connect_to_DB()
    sql_stmt = 'SELECT * from dbo.SUBJECTS st where st.SUBJECT = ?'
    cursor.execute(sql_stmt, subject)  
    row = cursor.fetchone()

    return row

def processUploadedFile(uploadedFile, fileType):
    fileDF = pandas.DataFrame()
    if fileType == 'text/csv':
        fileDF = pandas.read_csv(uploadedFile, parse_dates=True, dayfirst=True)
        # First convert datetime columns
        fileDF = fileDF.apply(lambda col: pandas.to_datetime(col, dayfirst=True, errors='ignore') 
              if col.dtypes == object 
              else col, 
              axis=0)
        # Then convert string columns
        fileDF = fileDF.apply(lambda col: col.astype('string')
              if col.dtypes == object 
              else col, 
              axis=0)
    else:
        fileDF = pandas.read_excel(uploadedFile)

    return fileDF
