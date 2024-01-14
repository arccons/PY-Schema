import pandas
import SchemaCheck.src.DBpkg as DBpkg

def checkSubject(subject):
    return DBpkg.checkSubject(subject)

def getSubjectList():
    return pandas.DataFrame.from_records(DBpkg.getSubjectList(), columns=['SUBJECT', 'TABLE_NAME'])

def createSubjectBase(fileDF, tableName, subject):
    tablesExist = DBpkg.createSubjectBase(tableName, subject)
    if not tablesExist:
        return False

    #print(f"File data types: \n{fileDF.dtypes}")
    #print(f"File columns: \n{fileDF.columns}")
    for col in fileDF.columns:
        colType = fileDF[col].dtypes
        if colType == 'float64':
            DBpkg.addFloatColumn(tableName, col)
        elif colType == 'int64':
            DBpkg.addIntColumn(tableName, col)
        elif colType == 'bool':
            DBpkg.addBoolColumn(tableName, col)
        elif colType == 'string':
            DBpkg.addStringColumn(tableName, col)
        elif colType == 'datetime64[ns]':
            DBpkg.addDateColumn(tableName, col)

    return True

def getTableColumns(table):
    return pandas.DataFrame.from_records(DBpkg.getTableColumns(table), columns=['ordinal','col', 'data_type'])

def processUploadedFile(uploadedFile, fileType):
    fileDF = pandas.DataFrame()
    if fileType == 'text/csv':
        fileDF = pandas.read_csv(uploadedFile, parse_dates=True, dayfirst=True)
    else:
        fileDF = pandas.read_excel(uploadedFile)
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

    return fileDF

def addFileRecords(fileDF, subject):
    stgTable = DBpkg.getTable(subject) + '_STG'
    tableDF = pandas.DataFrame.from_records(DBpkg.getTableColumns(stgTable), columns=['ORDINAL_POSITION', 'column_name', 'data_type'])
    #print(type(tableDF.columns), tableDF.columns)
    stgTableCols = [elem[1] for elem in tableDF.values.tolist()]
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
    DBpkg.addRecords(stgTable, stgTableCols[3:], fileValues)
    return True
