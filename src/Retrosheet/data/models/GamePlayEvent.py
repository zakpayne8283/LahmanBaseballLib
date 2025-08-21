from Retrosheet.data.models.retrosheet_table import RetrosheetTable

class GamePlayEvent(RetrosheetTable):

    # Name of the table in the DB
    db_table_name = "GamePlayEvents"

    # Each field and its information in the DB
    fields = {
        "play_id": "INT IDENTITY(1,1) PRIMARY KEY",
        "game_id": "NVARCHAR(12)",  # TODO: Foreign Key reference?
        "inning":  "TINYINT",
        "bottom_of_inning": "BIT",
        "batter_id": "NVARCHAR(8)",
        "pitcher_id": "NVARCHAR(8)"
    }

    def __init__(self, game_id, inning, bottom_inning, batter_id, pitcher_id):
        self.play_id = None
        self.game_id = game_id
        self.inning = inning
        self.bottom_of_inning = bottom_inning
        self.batter_id = batter_id
        self.pitcher_id = pitcher_id