from datetime import date

from Retrosheet.data.models.retrosheet_table import RetrosheetTable

class StartingLineup(RetrosheetTable):

    # Name of the table in the DB
    db_table_name = "StartingLineups"

    # Each field and its information in the DB
    fields = {
        "lineup_id": "INT IDENTITY(1,1) PRIMARY KEY",
        "game_id": "NVARCHAR(12)",  # TODO: Foreign Key reference?
        "team_id": "NVARCHAR(3)",
        "home_team": "BIT",         # BIT is a boolean; 0=away, 1=home
        "lineup_slot_1": "NVARCHAR(8)",
        "lineup_slot_2": "NVARCHAR(8)",
        "lineup_slot_3": "NVARCHAR(8)",
        "lineup_slot_4": "NVARCHAR(8)",
        "lineup_slot_5": "NVARCHAR(8)",
        "lineup_slot_6": "NVARCHAR(8)",
        "lineup_slot_7": "NVARCHAR(8)",
        "lineup_slot_8": "NVARCHAR(8)",
        "lineup_slot_9": "NVARCHAR(8)",
        "starting_p": "NVARCHAR(8)",
        "starting_c": "NVARCHAR(8)",
        "starting_1b": "NVARCHAR(8)",
        "starting_2b": "NVARCHAR(8)",
        "starting_3b": "NVARCHAR(8)",
        "starting_ss": "NVARCHAR(8)",
        "starting_lf": "NVARCHAR(8)",
        "starting_cf": "NVARCHAR(8)",
        "starting_rf": "NVARCHAR(8)",
        "starting_dh": "NVARCHAR(8)",
    }

    def __init__(self, game_id, team_id, home_team):
        # Since this is an IDENTITY, set it none and let the DB handle it
        self.lineup_id = None

        self.game_id = game_id
        self.team_id = team_id
        self.home_team = home_team

    def set_player_in_batting_order(self, player_id, order_number):
        # If the lineup slot hasn't been filled yet,
        if getattr(self, f"lineup_slot_{order_number}", None) is None:
            # Fill it
            setattr(self, f"lineup_slot_{order_number}", player_id)
        else:
            raise Exception("Attempted to start two players at the same lineup slot")

    def set_player_starting_position(self, player_id, starting_position):
        # TODO: Move the positions elsewhere where they can be reused?
        positions = ["p", "c", "1b", "2b", "3b", "ss", "lf", "cf", "rf", "dh"]

        # If the starting position hasn't been filled
        if getattr(self, f"starting_{positions[int(starting_position)-1]}", None) is None:
            # Fill it
            setattr(self, f"starting_{positions[int(starting_position)-1]}", player_id)
        else:
            raise Exception("Attempted to start two players at same position")