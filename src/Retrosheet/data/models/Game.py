from datetime import date

from Retrosheet.data.models.retrosheet_table import RetrosheetTable

class Game(RetrosheetTable):

    # Name of the table in the DB
    db_table_name = "Games"
    # Each field and its information in the DB
    fields = {
        "game_id": "NVARCHAR(12) PRIMARY KEY",
        "home_team": "NVARCHAR(3) NOT NULL",
        "away_team": "NVARCHAR(3) NOT NULL",
        "game_date": "DATE",        # YYYY-MM-DD
        "game_number": "TINYINT"    # Number played that day (0=only game, 1=first of double header, 2=second of double header)
    }

    def __init__(self, game_id):
        self.game_id = game_id

    def set_home_team(self, home_team: str):
        self.home_team = home_team

    def set_away_team(self, away_team: str):
        self.away_team = away_team

    def set_game_date(self, game_date: date):
        # Force it to be a date object in a specific format
        if not isinstance(game_date, date):
            raise TypeError("Game() Error - game_date must be a date(YYYY-MM-DD) object")

        print(game_date)

        self.game_date = date.strftime(game_date, "%Y-%m-%d")

    def set_game_number(self, game_number: int):
        self.game_number = game_number
    