from db.connector import get_connection

class TableBase:
    table_prefix = "dbo"
    table_name = ""
    table_name_full = ""

    connection = None
    cursor = None

    ###
    # Constructor:
    #   Setup DB connection
    #   Define full table name (prefix + table_name)
    ###
    def __init__(self):
        # Initialize the connection to be used
        self.connection = get_connection()
        self.cursor = self.connection.cursor()

        # Setup the full table names
        self.table_name_full = self.table_prefix + "." + self.table_name

    ###
    # SELECT Wrapper:
    #   Runs a select with a possible where clause
    ###
    def select(self, where_clause="", params=()):

        # Build query string
        sql = f"SELECT TOP 1000 * FROM {self.table_name_full}" #TODO: Remove "TOP 1000", just used for testing

        # Add optional where clause
        if where_clause:
            sql += f" WHERE {where_clause}"

        # Execute query
        self.cursor.execute(sql, params)
        
        # Return rows as result
        return self.cursor.fetchall()