# Query class used in the base_table class to better structure SQL queries
class Query:

    # Constructor
    #   table_class is the parent class for this query
    def __init__(self, table_class):
        self.table_class = table_class
        self.filters = {}
        self._limit = None

    # Where filter
    #   translates to SQL's `WHERE X = Y` later
    def where(self, **_filters):
        self.filters.update(_filters)
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

        # Setup base SQL select
        # Add the TOP(N) if limit is set
        sql = f"SELECT {f"TOP ({self._limit})" if self._limit is not None else ""} * FROM {self.table_class.table_name_full()}"

        # Build the filters and the where conditions in the SQL query
        params = []
        if self.filters:
            conditions = []
            for col, val in self.filters.items():
                conditions.append(f"{col} = ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(conditions)

        # Execute the query
        cursor.execute(sql, params)

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