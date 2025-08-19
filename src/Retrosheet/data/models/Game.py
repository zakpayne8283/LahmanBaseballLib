from Retrosheet.data.models.retrosheet_table import RetrosheetTable

class Game(RetrosheetTable):

    # Name of the table in the DB
    db_table_name = "Games"
    # Each field and its information in the DB
    fields = {
        "game_id": "NVARCHAR(12) PRIMARY KEY",
        "home_team": "NVARCHAR(3) NOT NULL",
        "away_team": "NVARCHAR(3) NOT NULL"
    }

    def __init__(self, game_id):
        self.game_id = game_id

    def set_home_team(self, home_team):
        self.home_team = home_team

    def set_away_team(self, away_team):
        self.away_team = away_team
    