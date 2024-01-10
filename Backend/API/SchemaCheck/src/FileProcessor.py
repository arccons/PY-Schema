import pandas
import SchemaCheck.src.MSsql as MSsql

def checkSubject(subject):
    return MSsql.checkSubject(subject)

def getSubjectList():
    rowList = MSsql.getSubjectList()
    print(f"Subject List = {rowList}")
    return pandas.DataFrame.from_records(rowList, columns=['SUBJECT'])

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

def getTableColumns(subject):
    return pandas.DataFrame.from_records(MSsql.getTableColumns(subject), columns=['ordinal','col', 'data_type'])

def createDBobjects(fileDF, tableName, subject):
    MSsql.createDBobjects(tableName, subject)
    subject_table_stg = tableName + '_STG'
    print(f"{subject_table_stg}")
    print(f"File data types: \n{fileDF.dtypes}")
    for item in fileDF.dtypes:
        print(f"item = {item}")
        if item == 'float64':
            MSsql.addFloatColumn(tableName, item)
            MSsql.addFloatColumn(subject_table_stg, item)
        elif item == 'int64':
            MSsql.addIntColumn(tableName, item)
            MSsql.addIntColumn(subject_table_stg, item)
        elif item == 'bool':
            MSsql.addBoolColumn(tableName, item)
            MSsql.addBoolColumn(subject_table_stg, item)
        elif item == 'string[Python]':
            MSsql.addStringColumn(tableName, item)
            MSsql.addStringColumn(subject_table_stg, item)
        elif item == 'datetime[ns]':
            MSsql.addDateColumn(tableName, item)
            MSsql.addDateColumn(subject_table_stg, item)

    return True

def addFileRecords(tableDF):
    return MSsql.addFileRecords(tableDF)
