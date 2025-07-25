# Query class used in the base_table class to better structure SQL queries
class Query:

    # Constructor
    #   table_class is the parent class for this query
    def __init__(self, table_class):
        self.table_class = table_class
        self.filters = {}
        self._limit = None
        self.orders = {}

    # Where filter
    #   translates to SQL's `WHERE X = Y` later
    def where(self, **_filters):
        self.filters.update(_filters)
        return self
    
    # Order By filter
    #   Specificies which field(s) to order by and the order
    def order_by(self, **_orders):
        self.orders.update(_orders)
        return self
    
    # Limit filter
    #   translates to TOP(N) later
    def limit(self, n):
        self._limit = n
        return self
    
    # Executes the query
    def execute(self):
        # Get the cursor from parent class
        cursor = self.table_class.get_cursor()

        # Limit string
        limit_string = f"TOP ({self._limit})" if self._limit is not None else ""

        # Setup base SQL select
        sql = f"SELECT {limit_string} * FROM {self.table_class.table_name_full()}"

        # Build the filters and the where conditions in the SQL query
        params = []
        if self.filters:
            conditions = []
            for col, val in self.filters.items():
                conditions.append(f"{col} = ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(conditions)

        # Add applicable orders, if they exist
        if self.orders:
            order_bys = []
            for field, direction in self.orders.items():
                order_bys.append(f"{field} {direction.upper()}")

            sql += " ORDER BY " + ", ".join(order_bys)

        # Execute the query
        try:
            cursor.execute(sql, params)
        except Exception as e:
            print(f"!!== ERROR: {e}")
            exit()

        # Get the column and rows
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        # Return instances of the subclass, with attributes set
        results = []

        # Put results in a list as objects
        for row in rows:
            # Pack the data, create a new object, and store it
            data = dict(zip(columns, row))
            instance = self.table_class(**data)
            results.append(instance)

        # Return the list of data
        return results