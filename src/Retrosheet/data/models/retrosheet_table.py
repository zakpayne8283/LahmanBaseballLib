from utils.db.base_table import TableBase

import Retrosheet.data.config as retrosheet_config 

# TODO: Define some sort of DROP TABLE here so I don't need to manually do it.
class RetrosheetTable(TableBase):
    database_name = retrosheet_config.retrosheet_database_name
    db_table_name = None
    fields = None

    @classmethod
    def create_table(cls):
        """
        Creates a new table for the given class, if it's not already present in the database.
        """

        if cls.db_table_name is None or cls.fields is None:
            raise NotImplementedError("Attempted table creation for non-tabular class.")
        
        # For each field in the class, create the table definition of that field
        field_definitions = ", ".join(f"{field_name} {definition}" for field_name, definition in cls.fields.items())

        creation_string = f"""
                IF NOT EXISTS (
                    SELECT 1
                    FROM sys.tables
                    WHERE name = '{cls.db_table_name}'
                    AND schema_id = SCHEMA_ID('dbo')
                )
                BEGIN
                    CREATE TABLE {cls.db_table_name} (
                        {field_definitions}
                    );
                END;
               """
    
        # Get the DB cursor
        cursor = cls.get_cursor()

        # Create the table
        cursor.execute(creation_string)

    def insert_into_db(self):
        """
        Inserts a new row in the database 
        """
        # Build our list of columns
        columns = ", ".join(self.fields.keys())

        # Build the corresponding list of values for that column
        values = ", ".join([
            self._format_value(getattr(self, field), self.fields[field]) # Format the value as needed
            for field in self.fields.keys()
        ])

        # SQL insert statement
        sql = f"INSERT INTO {self.db_table_name} ({columns}) VALUES ({values})"
        
        self.get_cursor().execute(sql)

    def _format_value(self, value: any, field_definition: str):
        """
        Format a value for SQL insertion based on its field type.
        """
        # NULL works better than None for DBs
        if value is None:
            return "NULL"

        # Put '' around the value if the field is VARCHAR, CHAR, or TEXT
        if "NVARCHAR" in field_definition.upper() or "CHAR" in field_definition.upper() or "TEXT" in field_definition.upper():
            return f"'{value}'"
        
        return value
