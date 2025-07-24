from db.models.base_table import TableBase

class AllstarAppearances(TableBase):
    
    def __init__(self):
        self.table_name = "AllstarFull"
        super().__init__()