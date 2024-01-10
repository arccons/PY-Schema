import pyodbc

def connect_to_DB():
    DBconn = pyodbc.connect(driver='{SQL Server}', server='DESKTOP-ALT0UH5', database='SchemaCheck', trusted_connection='yes')
    cursor = DBconn.cursor()
    return cursor

def getSubjectList():
    cursor = connect_to_DB()
    sql_stmt = "SELECT DISTINCT SUBJECT from SchemaCheck.dbo.SUBJECTS"
    print(f"SUBJECTS List = {sql_stmt}")
    cursor.execute(sql_stmt)  
    rowList = cursor.fetchall()
    return rowList

def checkSubject(subject):
    cursor = connect_to_DB()
    sql_stmt = f"SELECT st.SUBJECT from SchemaCheck.dbo.SUBJECTS st where st.SUBJECT = '{subject}'"
    #print(f"Column List = {sql_stmt}")
    cursor.execute(sql_stmt)
    row = cursor.fetchone()
    if row == None:
        return False
    return True

def getTable(subject):
    cursor = connect_to_DB()
    sql_stmt = f"SELECT st.TABLE_NAME from SchemaCheck.dbo.SUBJECTS st where st.SUBJECT = '{subject}'"
    #print(f"Column List = {sql_stmt}")
    cursor.execute(sql_stmt)
    row = cursor.fetchone()
    return row[0]

def getTableColumns(subject):
    cursor = connect_to_DB()
    table = getTable(subject)
    sql_stmt = f"SELECT col.ORDINAL_POSITION,  col.column_name, col.data_type from INFORMATION_SCHEMA.COLUMNS col where col.TABLE_NAME = '{table}' ORDER BY col.ORDINAL_POSITION"
    #print(f"Column List = {sql_stmt}")
    cursor.execute(sql_stmt)
    col_list = cursor.fetchall()
    print(f"Table columns = {col_list}")
    return col_list

def createDBobjects(tableName, subject):
    cursor = connect_to_DB()
    sql_subject_insert = f"INSERT INTO SchemaCheck.dbo.SUBJECTS (SUBJECT, TABLE_NAME) VALUES ('{subject}', '{tableName}')"
    print(f"New SUBJECT = {sql_subject_insert}")
    cursor.execute(sql_subject_insert)
    sql_table_create = f"CREATE TABLE SchemaCheck.dbo.{tableName} ([ID] [uniqueidentifier] NOT NULL, [LOAD_TIMESTAMP] [timestamp] NOT NULL)"
    print(f"New Subject Table = {sql_table_create}")
    cursor.execute(sql_table_create)
    subject_table_stg = tableName + '_STG'
    sql_table_stg_create = f"CREATE TABLE SchemaCheck.dbo.{subject_table_stg} ([ID] [uniqueidentifier] NOT NULL, [STATUS] [char](10) NOT NULL, [STATUSTIMESTAMP] [timestamp] NOT NULL)"
    print(f"New Staging Table = {sql_table_stg_create}")
    cursor.execute(sql_table_stg_create)
    return True

def addStringColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD ({colName} varchar(255))"
    print(f"Add column = {sql_add_col}")
    cur.execute(sql_add_col)
    return True

def addFloatColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD ({colName} float)"
    print(f"Add column = {sql_add_col}")
    cur.execute(sql_add_col)
    return True

def addIntColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD ({colName} numeric)"
    print(f"Add column = {sql_add_col}")
    cur.execute(sql_add_col)
    return True

def addBoolColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD ({colName} char)"
    print(f"Add column = {sql_add_col}")
    cur.execute(sql_add_col)
    return True

def addDateColumn(table, colName):
    cur = connect_to_DB()
    sql_add_col = f"ALTER TABLE {table} ADD ({colName} datetime)"
    print(f"Add column = {sql_add_col}")
    cur.execute(sql_add_col)
    return True

def addFileRecords(tableDF):
    return True
