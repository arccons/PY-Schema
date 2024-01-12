import pandas
import SchemaCheck.src.MSsql as MSsql

def checkSubject(subject):
    return MSsql.checkSubject(subject)

def getSubjectList():
    return pandas.DataFrame.from_records(MSsql.getSubjectList(), columns=['SUBJECT'])

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

def getTableColumns(table):
    return pandas.DataFrame.from_records(MSsql.getTableColumns(table), columns=['ordinal','col', 'data_type'])

def createSubjectBase(fileDF, tableName, subject):
    tablesExist = MSsql.createSubjectBase(tableName, subject)
    if not tablesExist:
        return False

    print(f"File data types: \n{fileDF.dtypes}")
    print(f"File columns: \n{fileDF.columns}")
    for col in fileDF.columns:
        colType = fileDF[col].dtypes
        print(f"Column type = {colType}")
        if colType == 'float64':
            MSsql.addFloatColumn(tableName, col)
        elif colType == 'int64':
            MSsql.addIntColumn(tableName, col)
        elif colType == 'bool':
            MSsql.addBoolColumn(tableName, col)
        elif colType == 'string':
            MSsql.addStringColumn(tableName, col)
        elif colType == 'datetime64[ns]':
            MSsql.addDateColumn(tableName, col)

    return True

def addFileRecords(fileDF, subject):
    stgTable = MSsql.getTable(subject) + '_STG'
    tableDF = pandas.DataFrame.from_records(MSsql.getTableColumns(stgTable), columns=['ORDINAL_POSITION', 'column_name', 'data_type'])
    #stgTableRow = MSsql.getTableColumns(stgTable)
    #row_to_list = [elem for elem in row]
    stgTableCols = [elem[1] for elem in tableDF.values.tolist()]
    #print(f"Staging table columns type = {type(stgTableCols)}")
    #print(f"Staging table columns = {stgTableCols}")
    fileCols = fileDF.columns.tolist()
    #print(f"File DF columns type = {type(fileCols)}")
    #print(f"File DF columns = {fileCols}")
    tableColNum = len(stgTableCols)
    fileColNum = len(fileCols)
    #print(f"Number of table columns = {tableColNum - 3}")
    #print(f"Number of file columns = {fileColNum}")
    if ((tableColNum-3) != fileColNum):
        return False
    fileValues = fileDF.values
    #print(f"fileDF = \n{fileDF}")
    #print(f"File DF items = \n{fileValues}")
    MSsql.addRecords(stgTable, stgTableCols[3:], fileValues)
    return True
