import pyodbc

_connection = None

def get_connection(database_name, enable_autocommit=False):
    global _connection

    if _connection is None:
        _connection = pyodbc.connect(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=localhost\SQLEXPRESS;'
            f'DATABASE={database_name};'
            r'Trusted_Connection=yes;',
            autocommit=enable_autocommit
    )
        
    return _connection