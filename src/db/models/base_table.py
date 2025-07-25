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
    def select(cls, **filters):
        cls._query = Query(cls).where(**filters)
        return cls._query
    
    # Static method for adding ORDERBY to a query
    @classmethod
    def order_by(cls, **orders):
        if cls._query is None:
            raise Exception("ERROR - no existing query. Ensure you've run `select()` first.")
        
        cls._query = cls._query.order_by(**orders)
        return cls._query
    
    # Static method for adding a limit to rows returned
    @classmethod
    def limit(cls, n):
        if cls._query is None:
            raise Exception("ERROR - no existing query. Ensure you've run `select()` first.") 
        
        cls._query = cls._query.limit(n)
        return cls._query

    # Static method for JOIN on the current query
    @classmethod
    def join(cls, other_table, **join_ons):
        if cls._query is None:
            raise Exception("ERROR - no existing query. Ensure you've run `select()` first.") 
        
        cls._query = cls._query.join(other_table, **join_ons)
        return cls._query

    # Static method for setting up groupings
    def group_by(cls, groupings):
        if cls._query is None:
            raise Exception("ERROR - no existing query. Ensure you've run `select()` first.")
        
        cls._query = cls._query.group_by(groupings)
        return cls._query

    # Aggregation functions are done here
    def aggregate(cls, **aggregations):
        if cls._query is None:
            raise Exception("ERROR - no existing query. Ensure you've run `select()` first.")
        
        cls._query = cls._query.aggregate(**aggregations)
        return cls._query

    # Static method for executing a query
    @classmethod
    def execute(cls):
        cls._query.execute()