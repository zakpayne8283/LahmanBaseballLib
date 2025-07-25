from types import SimpleNamespace

# Query class used in the base_table class to better structure SQL queries
class Query:

    # Constructor
    #   table_class is the parent class for this query
    def __init__(self, table_class):
        # Base table the query is being made on
        self.table_class = table_class

        # Aggregation functions to run
        self.aggregations = {}

        # The columns being selected
        self.columns = []

        # The where clauses - only supports ANDs right now
        self.filters = {}

        # The field(s) that will be grouped at the end
        self.groupings = []

        # Tables to join on in the query
        self.joins = {}

        # Limit the number of items in the query
        self._limit = None

        # Which fields to order by
        self.orders = {}

    # Where filter
    #   translates to SQL's `WHERE X = Y` later
    def where(self, **_filters):
        self.filters.update(_filters)
        return self
    
    # Order By filter
    #   Specificies which field(s) to order by and the order
    #   Data provided as fieldName=orderDirection (e.g. nameFirst=ASC)
    def order_by(self, **_orders):
        self.orders.update(_orders)
        return self
    
    # Limit filter
    #   translates to TOP(N) later
    def limit(self, n):
        self._limit = n
        return self
    
    # Join
    #   most basic join with which field(s) to join on
    #   Expects data as other_table->class; field="fieldname" (e.g. .join(People, "playerID"))
    def join(self, other_table, field):
        self.joins.update({other_table.table_name_full():field})
        return self
    
    # Group By
    #   What fields should be grouped
    def group_by(self, groupings):
        if not isinstance(groupings, list):
            raise ValueError("Parameter `groupings` must be a list")

        self.groupings = groupings
        self.columns = list(dict.fromkeys(self.columns + groupings))
        return self
    
    # Aggregate
    #   Maps a given field to an aggregation function
    def aggregate(self, **aggregations):
        self.aggregations.update(aggregations)
        return self

    # Executes the query
    def execute(self):
        # Get the cursor from parent class
        cursor = self.table_class.get_cursor()

        # Limit string
        limit_string = f" TOP ({self._limit})" if self._limit is not None else ""

        # Specifiy the columns we're selecting
        # Right now just do all
        query_columns = ""
        if self.columns and not self.joins:
            query_columns = ",".join(self.columns)
        elif self.columns and self.joins:
            # TODO: Add support for the joining table
            query_columns = ",".join([self.table_class.table_name_full() + "." + c for c in self.columns])
        else:
            query_columns = " * "

        # Add the aggregations as needed
        # for each key in self.aggrgations, generate SQL that corresponds to each list item's key's value with AS being the key
        # e.g {'count': [{'appearances': '*'}]} ==> COUNT (*) AS appearances
        if self.aggregations:
            agg_statements = []
            for func, fields in self.aggregations.items():
                for field in fields:
                    for alias, agg_col in field.items():
                        agg_statements.append(f"{func.upper()}({agg_col}) AS {alias}")
            
            query_columns += ", " + ",".join(agg_statements)

        # Setup base SQL select
        sql = f"SELECT {limit_string} {query_columns} FROM {self.table_class.table_name_full()}"

        # Join tables, as needed
        if self.joins:
            #TODO: Support more than one join here
            join_statements = []
            for table, column in self.joins.items():
                join_statements.append(f" JOIN {table} on {self.table_class.table_name_full()}.{column} = {table}.{column}")
            
            sql += "".join(join_statements)

        # Build the filters and the where conditions in the SQL query
        params = []
        if self.filters:
            conditions = []
            for col, val in self.filters.items():
                conditions.append(f"{col} = ?")
                params.append(val)
            sql += " WHERE " + " AND ".join(conditions)

        # Add groupings here, as needed
        if self.groupings:
            if self.joins:
                self.groupings = [self.table_class.table_name_full() + "." + c for c in self.groupings]

            sql += " GROUP BY " + ",".join(self.groupings)

        # Add applicable orders, if they exist
        if self.orders:
            order_bys = []
            for field, direction in self.orders.items():
                order_bys.append(f"{field} {direction.upper()}")

            sql += " ORDER BY " + ", ".join(order_bys)

        print("SQL Statement Being Run ------")
        print(sql)

        # Execute the query
        try:
            cursor.execute(sql, params)
        except Exception as e:
            print(f"!!== ERROR: {e}")
            exit()

        # Get the column and rows
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        # Results should only be an instance if we're selecting the full data
        # TODO: Maybe there's a way to still return the whole objects?
        results_as_instance = False if self.joins or self.columns or self.aggregations else True

        # Return instances of the subclass, with attributes set
        results = []

        # Put results in a list as objects
        for row in rows:
            # Pack the data, create a new object, and store it
            data = dict(zip(columns, row))
            instance = self.table_class(**data) if results_as_instance is True else SimpleNamespace(**data)
            results.append(instance)

        # Return the list of data
        return results