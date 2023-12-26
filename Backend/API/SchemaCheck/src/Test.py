import pandas
import SchemaCheck.src.MSsql as MSsql

def getFileSubject(subject):
    cursor = MSsql.connect_to_DB()
    sql_stmt = 'SELECT * from dbo.SUBJECTS st where st.SUBJECT = ?'
    cursor.execute(sql_stmt, subject)  
    row = cursor.fetchone()

    return row

def processUploadedFile(uploadedFile, fileType, subject):
    fileDF = pandas.DataFrame()
    if fileType == 'text/csv':
        fileDF = pandas.read_csv(uploadedFile)
    else:
        print(fileType)
        fileDF = pandas.read_excel(uploadedFile)

    print(fileDF)
            
    return fileDF.dtypes
