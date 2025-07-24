from db.connector import get_connection

class TableBase:

    _connection = None

    # Static method for getting the DB connection in the models
    @classmethod
    def get_connection(cls):
        # setup connection as needed
        if cls._connection is None:
            cls._connection = get_connection()
        
        # return it
        return cls._connection

    # Static method for getting the DB connection cursor
    @classmethod
    def get_cursor(cls):
        return cls.get_connection().cursor()
    
    # Static method used by CHILDREN to define table name
    @classmethod
    def table_name(cls):
        raise NotImplementedError("Must define table_name in subclass")
    
    # Static method to combine the prefix with the table name
    @classmethod
    def table_name_full(cls):
        return "dbo." + cls.table_name() #TODO: Add flexability for table_prefix

    # Static method for making select statements
    @classmethod
    def select(cls, where_clause="", params=()):

        # Build query string
        sql = f"SELECT TOP 1000 * FROM {cls.table_name_full()}" #TODO: Remove "TOP 1000", just used for testing

        # Add optional where clause
        if where_clause:
            sql += f" WHERE {where_clause}"

        # Execute query
        cursor = cls.get_cursor()
        cursor.execute(sql, params)
        
        # Return rows as result
        return cursor.fetchall()