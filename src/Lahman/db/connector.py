import pyodbc

_connection = None

# TODO: Move to an .env file or something
database_name = "lahman2024"

def get_connection():
    global _connection

    if _connection is None:
        _connection = pyodbc.connect(
            r'DRIVER={ODBC Driver 17 for SQL Server};'
            r'SERVER=localhost\SQLEXPRESS;'
            f'DATABASE={database_name};'
            r'Trusted_Connection=yes;'
    )
        
    return _connection