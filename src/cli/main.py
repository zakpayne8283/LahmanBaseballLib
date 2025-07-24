import argparse
import pyodbc

# TODO: Move to an .env file or something
database_name = "lahman2024"

def main():
    print("Starting main function...")

    conn = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=localhost\SQLEXPRESS;'
        f'DATABASE={database_name};'
        r'Trusted_Connection=yes;'
    )

    cursor = conn.cursor()
    cursor.execute("SELECT TOP 5 * FROM dbo.AllstarFull")
    rows = cursor.fetchall()

    for row in rows:
        print(row)


if __name__ == '__main__':
    main()