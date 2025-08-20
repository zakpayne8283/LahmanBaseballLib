from datetime import date

from Retrosheet.data.models.retrosheet_table import RetrosheetTable

class StartingLineup(RetrosheetTable):

    # Name of the table in the DB
    db_table_name = "StartingLineup"

    # Each field and its information in the DB
    fields = {
        "lineup_id": "INT IDENTITY(1,1) PRIMARY KEY",
        "game_id": "NVARCHAR(12)",  # TODO: Foreign Key reference?
        "team_id": "NVARCHAR(3)",
        "home_team": "BIT"          # BIT is a boolean; 0=away, 1=home
    }

    def __init__(self, game_id, team_id, home_team):
        # Since this is an IDENTITY, set it none and let the DB handle it
        self.lineup_id = None
        
        self.game_id = game_id
        self.team_id = team_id
        self.home_team = home_team