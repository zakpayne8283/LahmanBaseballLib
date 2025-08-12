from types import SimpleNamespace

# Query class used in the base_table class to better structure SQL queries
class Query:
    # To build out sub-queries, I'll need to do the following:
    # - add a HAVING statement, which can also take Query() objects
    # - Modify SELECT to accept subqueries
    # TODO: Add correlated subqueries 

    # Constructor
    #   table_class is the parent class for this query
    def __init__(self, from_table):
        # Base table or query the query is being made on (FROM)
        self.from_table = from_table

        # Aggregation functions to run
        self.aggregations = {}

        # The columns being selected
        self.columns = []

        # The where clauses - only supports ANDs right now
        self.wheres = {}

        # The field(s) that will be grouped at the end
        self.groupings = []

        # The having to tack on at the end
        # TODO: Make this able to cover more than just the last GROUP BY
        self.havings = {}

        # Tables to join on in the query
        self.joins = {}

        # Limit the number of items in the query
        self._limit = None

        # Which fields to order by
        self.orders = {}

        # Optionally set an "AS" name for a subquery
        self.query_name = None

        # Optionally enable a table alias for queries
        self.table_alias = None

    # Select statement
    #   chooses which columns to display from the parent table
    #   TODO: Update this to accept columns from joined tables?
    #   Expects columns as strings (e.g.) .select("nameFirst")
    def select(self, *columns):
        self.columns.extend(columns)
        return self
    
    # AS statement
    #   Takes a string and set it as the self.query_name value
    #   This is so parent queries can reference this query
    def as_name(self, name):
        self.query_name = name
        return self
    
    # Table Alias
    #   Takes a string and uses it as an alias for the current table being used
    def alias(self, alias_name):
        self.table_alias = alias_name
        return self

    # Build the WHERE of where data is coming from
    def _build_from_query(self):
        # If the FROM table is a query, we need to recursively generate that query too.
        if isinstance(self.from_table, Query):
            #TODO: Refactor so this has just one return
            as_query = f" AS {self.from_table.query_name}" if self.from_table.query_name is not None else ""
            return f"FROM ({self.from_table.build_query()}){as_query}"
        else:
            alias_string = f" {self.table_alias} " if self.table_alias is not None else ""
            return f"FROM {self.from_table.table_name_full()}{alias_string}"

    # Build columns that are being selected
    def _build_columns_query(self):
        # Specifiy the columns we're selecting
        # Right now just do all
        # TODO:
        #   Maybe find a way this works a bit better, especially for joins - namely that you can do a join column here
        #   This also presents issues when doing a JOIN because common fields (e.g. playerID) are ambiguous during selection
        # TODO: Right now I would have to specify the column names in full and that's a hassle
        if self.columns:
            return f" {",".join(self.columns)} "
        elif self.aggregations:
            # On no columns and aggregations, only include the aggregations
            return " "
        else:
            return " * "

    # WHERE queries
    #   translates to SQL's `WHERE X = Y` later
    #   Expects **_wheres as column=value (e.g.) .where(nameFirst="Alex")
    #   Also accepts comparison values: column__op=value (e.g.) .where(yearID__gt=1980) --> yearID > 1980
    def where(self, **_wheres):
        self.wheres.update(_wheres)
        return self
    
    # Build the WHERE queries
    def _build_where_query(self):
        if self.wheres:
            where_clauses = []
            # Loop through each WHERE clause
            for col, val in self.wheres.items():
                where_string = ""

                if isinstance(val, Query):
                    # The WHERE value is a query, and needs to be built
                    where_string = f"{col} IN ({val.build_query()})"
                else:
                    # The WHERE value is NOT a query, proceed as usual

                    # Setup the base clause
                    # TODO: Modify this to work with JOINs (e.g. where a.year > 1900 AND b.year < 2000)
                    where_string = f"{self._table_name()}."
                    # If __ is present in the column, apply an operator other than "=" to it
                    if "__" in col:
                        # Get the name and operation
                        column_options = col.split("__")

                        # Extract the name, should always be the first, removing from list
                        col_name = column_options.pop(0)

                        # Get the specific operation
                        # Code mappings
                        sql_op_codes = {"gt": ">", "gte": ">=", "lt": "<", "lte": "<=", "ne": "!=", "like": "LIKE", "in": "IN"}
                        # Get the operation, if we find it
                        sql_op = [sql_op_codes[code] for code in sql_op_codes if code in column_options]
                        # If we don't find it, just make it equals
                        sql_op = "=" if sql_op == [] else sql_op[0]

                        # Get if the WHERE value should be treated as a variable
                        is_var = "var" in column_options

                        # Finish the clause
                        # TODO Probably want some sort of check for val here at some point
                        where_string += f"{col_name} {sql_op} {str(val) if is_var is False else val}"
                    elif val == None:
                        where_string += f"{col} IS NULL"
                    else:
                        # Just give a basic where clause
                        where_string += f"{col} = '{str(val)}'"

                # Add the finished clause to our list
                where_clauses.append(where_string)

            # Add where clauses to the SQL query
            return " WHERE " + " AND ".join(where_clauses)
        else:
            return ""

    # Order By filter
    #   Specificies which field(s) to order by and the order
    #   Data provided as fieldName=orderDirection (e.g. nameFirst=ASC)
    def order_by(self, **_orders):
        self.orders.update(_orders)
        return self
    
    def _build_orderby_query(self):
        # Add applicable orders, if they exist
        if self.orders:
            order_bys = []
            for field, direction in self.orders.items():
                order_bys.append(f"{field} {direction.upper()}")

            return " ORDER BY " + ", ".join(order_bys)
        else:
            return ""

    # Limit filter
    #   translates to TOP(N) later
    #   Expects n as integer
    def limit(self, n):
        self._limit = n
        return self
    
    # Build limit filter SQL
    def _build_limit_query(self):
        if self._limit is not None:
            return f" TOP ({self._limit})"
        else:
            return ""

    # Join
    #   most basic join with which field(s) to join on
    #   Expects data as other_table->class; field="fieldname" (e.g. .join(People, "playerID"))
    def join(self, other_table, field):
        self.joins.update({other_table.table_name_full():field})
        return self
    
    # Build JOIN query
    def _build_join_query(self):
        # Join tables, as needed
        if self.joins:
            #TODO: Support more than one join here, specifically the ON statement
            join_statements = []
            for table, column in self.joins.items():
                this_table_and_column = f"{self._table_name()}.{column}"
                join_statements.append(f" JOIN {table} ON {this_table_and_column} = {table}.{column}")
            
            return "".join(join_statements)
        else:
            return ""

    # Group By
    #   What fields should be grouped
    #   Expects *groups as strings (e.g.) .group_by("playerID")
    def group_by(self, *groupings):
        # Add the groupings if they haven't already been added
        for group in groupings:
            if group not in self.groupings:
                self.groupings.append(group)

        # Update the columns selected
        self.columns = list(dict.fromkeys(self.columns + self.groupings))
        return self
    
    # Build GROUP BY query
    def _build_groupby_query(self):
        if self.groupings:
            return " GROUP BY " + ",".join(self.groupings)
        else:
            return ""

    # Aggregate
    #   Maps a given field to an aggregation function
    #   Expects **aggregations as (e.g.) count=[{"player": "*"}]
    def aggregate(self, **aggregations):
        self.aggregations.update(aggregations)
        return self

    # Build aggregated columns
    def _build_aggregates_query(self):
        # Add the aggregations as needed
        # for each key in self.aggrgations, generate SQL that corresponds to each list item's key's value with AS being the key
        # e.g {'count': [{'appearances': '*'}]} ==> COUNT (*) AS appearances
        if self.aggregations:
            agg_statements = []
            for func, fields in self.aggregations.items():
                for field in fields:
                    for alias, agg_col in field.items():
                        agg_statements.append(f"{func.upper()}({agg_col}) AS {alias}")
            
            return (", " if self.columns else "") + (",".join(agg_statements)) + " "
        else:
            return ""

    # Having
    #   Conditions on GROUP BY statements
    #   (e.g.) SELECT yearID, COUNT(*) FROM dbo.Allstars GROUP BY yearID HAVING COUNT(*) > 10 would return all ASGs with more than 10 players
    def having(self, **havings):
        self.havings.update(havings)
        return self

    # Build having statements
    def _build_having_query(self):
        # Add the having query as needed
        # for each key in self.havings, generate SQL for the given aggreagte function, matching the parameters
        # e.g {'count': [{'>': '10'}]} ==> COUNT (*) > 10
        if self.havings:
            having_statements = []
            # for each HAVING qualifer ('count': [{'>': '10'}])
            for aggregator, qualifier in self.havings.items():
                # For each of the havings we're checking in it [{'>': '10'}, {...}, ...]
                for having_set in qualifier:
                    # Get the operator ('>') and the value (10) and build the available HAVING statements
                    for operator, value in having_set.items():
                        # If the provided value is a query, build it first
                        if isinstance(value, Query):
                            as_statement = f" AS {value.query_name}" if value.query_name is not None else ""
                            value = f"({value.build_query()}){as_statement}"
                        # Append the new statement
                        having_statements.append(f"{aggregator.upper()}(*) {operator} {value}")
            
            return " HAVING " + "AND".join(having_statements)
        else:
            return ""

    # Build SQL query
    #   Builds the SQL query and returns it as a string, plus any where parameters
    #   TODO: Might be nice to break this into multiple methods for clarity?
    def build_query(self):

        # Build the query piece by piece
        sql = "SELECT"

        # Add limit statement (TOP(N))
        sql += self._build_limit_query()
        
        # Add specific columns to statement
        sql += self._build_columns_query()

        # Add aggregated columns to statement
        sql += self._build_aggregates_query()

        # Build the FROM string
        sql += self._build_from_query()

        # Build any JOIN queries
        sql += self._build_join_query()

        # Build any WHERE statements
        sql += self._build_where_query()

        # Build any GROUP BY statements
        sql += self._build_groupby_query()

        # Build any ORDER BY statements
        sql += self._build_orderby_query()

        # Build any HAVING statements
        sql += self._build_having_query()

        return sql

    # Executes the query
    def execute(self):
        # Get the cursor from base table class
        # TODO: Probably just want some sort of connector, not in a query-related class...?
        from db.models.base_table import TableBase
        cursor = TableBase.get_cursor()

        # Get the SQL and parameters
        sql = self.build_query()

        print("Running SQL query: ")
        print(sql)

        # Execute the query
        try:
            cursor.execute(sql)
        except Exception as e:
            print(f"!!== ERROR: {e}")
            exit()

        # Get the column and rows
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        # Results should only be an instance if we're selecting the full data
        # TODO: Maybe there's a way to still return the whole objects?
        results_as_instance = False if self.joins or self.columns or self.aggregations or isinstance(self.from_table, Query) else True

        # Return instances of the subclass, with attributes set
        results = []

        # Put results in a list as objects
        for row in rows:
            # Pack the data, create a new object, and store it
            data = dict(zip(columns, row))
            instance = self.from_table(**data) if results_as_instance is True else SimpleNamespace(**data)
            results.append(instance)

        # Return the list of data
        return results
    
    def _table_name(self):
        if self.table_alias:
            return self.table_alias
        
        return self.from_table.table_name_full()