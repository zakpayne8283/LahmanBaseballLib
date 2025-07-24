from db.models.base_table import TableBase

class AllstarAppearances(TableBase):
    
    @classmethod
    def table_name(cls):
        return "AllstarFull"