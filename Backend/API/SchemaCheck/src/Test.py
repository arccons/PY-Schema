import pandas
import SchemaCheck.src.MSsql as MSsql

def testFile(subject):
    cursor = MSsql.connect_to_DB()
    sql_stmt = 'SELECT * from dbo.SUBJECTS st where st.SUBJECT = ?'
    cursor.execute(sql_stmt, subject)  
    row = cursor.fetchone()

    return row

def processUploadedFile(uploadedFile, fileType, subject):
    row = testFile(subject)
    if not row:
        return None
    fileDF = pandas.DataFrame()
    if fileType == 'text/csv':
        fileDF = pandas.read_csv(uploadedFile)
    else:
        print(fileType)
        fileDF = pandas.read_excel(uploadedFile)

    return fileDF.dtypes
