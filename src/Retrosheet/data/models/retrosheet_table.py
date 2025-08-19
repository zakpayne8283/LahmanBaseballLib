from utils.db.base_table import TableBase

import Retrosheet.data.config as retrosheet_config 

class RetrosheetTable(TableBase):
    database_name = retrosheet_config.retrosheet_database_name

    # TODO: Make this more flexible for future derived classes
    @classmethod
    def table_creation_wrapper(cls, table_name):
        return f"""
                IF NOT EXISTS (
                    SELECT 1
                    FROM sys.tables
                    WHERE name = '{table_name}'
                    AND schema_id = SCHEMA_ID('dbo')
                )
                BEGIN [TABLE_CREATION_SQL] END;
               """
