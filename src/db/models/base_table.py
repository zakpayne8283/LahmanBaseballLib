from db.connector import get_connection
from db.models.query_builder import Query

class TableBase:

    _connection = None
    _query = None

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
    # TODO: Move **fitlers out to a where() function and replace it with columns to select
    @classmethod
    def select(cls, *columns):
        cls._query = Query(cls).select(*columns)
        return cls._query
    