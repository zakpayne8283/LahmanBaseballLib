import pytest
from db.models.base_table import TableBase

def test_table_name():
    # Cannot have a table name if no table is provided
    with pytest.raises(NotImplementedError) as not_implemented:
        table = TableBase()
        table.table_name()