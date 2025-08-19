from Retrosheet.data.models.retrosheet_table import RetrosheetTable

class Game(RetrosheetTable):

    # Name of the table in the DB
    db_table_name = "Games"
    # Each field and its information in the DB
    fields = {
        "game_id": "NVARCHAR(12) PRIMARY KEY"
    }

    def __init__(self, game_id):
        self.game_id = game_id
    