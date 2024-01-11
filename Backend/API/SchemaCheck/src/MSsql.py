import pyodbc
from datetime import datetime, date

def connect_to_DB():
    DBconn = pyodbc.connect(driver='{SQL Server}', server='DESKTOP-ALT0UH5', database='SchemaCheck', trusted_connection='yes')
    cursor = DBconn.cursor()
    return cursor

def getSubjectList():
    cursor = connect_to_DB()
    sql_stmt = "SELECT DISTINCT SUBJECT from SchemaCheck.dbo.SUBJECTS"
    print(f"Subject List SQL = {sql_stmt}")
    cursor.execute(sql_stmt)  
    rowList = cursor.fetchall()
    return rowList

def checkSubject(subject):
    cursor = connect_to_DB()
    sql_stmt = f"SELECT st.SUBJECT from SchemaCheck.dbo.SUBJECTS st where st.SUBJECT = '{subject}'"
    #print(f"Subject SQL = {sql_stmt}")
    cursor.execute(sql_stmt)
    row = cursor.fetchone()
    if row == None:
        return False
    return True

def getTable(subject):
    cursor = connect_to_DB()
    sql_stmt = f"SELECT st.TABLE_NAME from SchemaCheck.dbo.SUBJECTS st where st.SUBJECT = '{subject}'"
    #print(f"Table SQL = {sql_stmt}")
    cursor.execute(sql_stmt)
    row = cursor.fetchone()
    return row[0]

def getTableColumns(table):
    cursor = connect_to_DB()
    #table = getTable(subject)
    sql_stmt = f"SELECT col.ORDINAL_POSITION, col.column_name, col.data_type from INFORMATION_SCHEMA.COLUMNS col where col.TABLE_NAME = '{table}' ORDER BY col.ORDINAL_POSITION"
    #print(f"Column List SQL = {sql_stmt}")
    cursor.execute(sql_stmt)
    col_list = cursor.fetchall()
    print(f"Table columns = {col_list}")
    return col_list

def createSubjectBase(tableName, subject):
    cursor = connect_to_DB()
    sql_subject_insert = f"INSERT INTO SchemaCheck.dbo.SUBJECTS (SUBJECT, TABLE_NAME) VALUES ('{subject}', '{tableName}')"
    print(f"New SUBJECT SQL = {sql_subject_insert}")
    cursor.execute(sql_subject_insert)
    sql_table_create = f"CREATE TABLE SchemaCheck.dbo.{tableName} ([ID] [uniqueidentifier] NOT NULL, [LOAD_TIMESTAMP] [timestamp] NOT NULL)"
    print(f"New Subject Table SQL = {sql_table_create}")
    cursor.execute(sql_table_create)
    subject_table_stg = tableName + '_STG'
    sql_table_stg_create = f"CREATE TABLE SchemaCheck.dbo.{subject_table_stg} ([ID] [uniqueidentifier] NOT NULL, [STATUS] [char](10) NOT NULL DEFAULT('LOADED'), [STATUSTIMESTAMP] [timestamp] NOT NULL)"
    print(f"New Staging Table SQL = {sql_table_stg_create}")
    cursor.execute(sql_table_stg_create)
    cursor.commit()
    return True

def addStringColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD {colName} varchar(255)"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    sql_add_col = f"ALTER TABLE {table}_STG ADD {colName} varchar(255)"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    cur.commit()
    return True

def addFloatColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD {colName} float"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    sql_add_col = f"ALTER TABLE {table}_STG ADD {colName} float"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    cur.commit()
    return True

def addIntColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD {colName} numeric"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    sql_add_col = f"ALTER TABLE {table}_STG ADD {colName} numeric"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    cur.commit()
    return True

def addBoolColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD {colName} bit"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    sql_add_col = f"ALTER TABLE {table}_STG ADD {colName} bit"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    cur.commit()
    return True

def addDateColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD {colName} datetime"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    sql_add_col = f"ALTER TABLE {table}_STG ADD {colName} datetime"
    print(f"Add column SQL = {sql_add_col}")
    cur.execute(sql_add_col)
    cur.commit()
    return True

def addRecords(table, colList, valList):
    cur = connect_to_DB()
    colString = 'ID, ' + ', '.join(colList)
    for item in valList:
        valString = f"NEWID()"
        for i in range(len(item)):
            itemString = ""

            isBool = False
            if item[i] in (True, False):
                itemString = str(1) if item[i] else str(0)
                isBool = True
            
            isDate = False
            if isinstance(item[i], datetime):
                itemString = f"{datetime.fromtimestamp(item[i])}"
                isDate = True
            
            isString = False
            if isinstance(item[i], str) and not isDate:
                itemString = f"'{item[i]}'"
                isString = True
            
            if not isDate and not isString and not isBool:
                itemString = str(item[i])

            valString = valString + ', ' + itemString
        print(f"Column string = {colString}; Value string = {valString}")
        sql_insert_record = f"INSERT INTO {table} ({colString}) VALUES({valString})"
        print(f"sql_insert_record = {sql_insert_record}")
        cur.execute(sql_insert_record)
    cur.commit()
    return True
