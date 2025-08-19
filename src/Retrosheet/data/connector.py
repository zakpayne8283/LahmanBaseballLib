import pyodbc

import Retrosheet.data.config as retrosheet_configs

_connection = None

# TODO: Move to an .env file or something
database_name = retrosheet_configs.retrosheet_database_name

def get_connection(enable_autocommit=False):
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