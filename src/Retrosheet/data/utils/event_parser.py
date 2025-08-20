from datetime import date, datetime

from Retrosheet.data.models.Game import Game as GameModel
from Retrosheet.data.models.StartingLineup import StartingLineup as StartingLineupModel

class EventParser:
    def __init__(self, file_path):
        # File location on disk
        self.file_path = file_path

        # Used to track game data
        self.current_game = None

        # Used when setting the lineups
        self.lineups = {}

        # Handler methods for handling certain inputs
        self.handlers = {
            "id": self.handle_id,
            "info": self.handle_info,
            "start": self.handle_start
        }

    def parse_event_file(self):
        """
        Parses the event file for this current EventParser
        """
        # Open the file
        with open(self.file_path, "r") as event_file:
            # Scan through each line
            for line in event_file:
                # Clean the data line and split it
                line_data = line.strip().split(",")
                # Get the operation for that line (id,info,play, etc.)
                operation = line_data[0]
                # Dispatch the operation to the correct handler
                handler = self.handlers.get(operation)
                if handler:
                    handler(line_data)
                else:
                    pass#print(f"Unknown operation: {operation}")
    
    # Sends all data to database
    def flush_game_to_db(self):
        # Send the current game to the DB
        self.current_game.insert_into_db()

        # Send each lineup to the DB
        for lineup in self.lineups.values():
            lineup.insert_into_db()

        # Reset necessary data
        self.current_game = None
        self.lineups = {}

    # Handles operation="id" -- start of new game
    def handle_id(self, line_data):
        # If we already have game data (not the first game we've scanned)
        # flush current to db, then carry on.
        if self.current_game:
            self.flush_game_to_db()

        # Get the game ID
        game_id = line_data[1]
        # Create a new game object
        self.current_game = GameModel(game_id=game_id)

    # Handles the various "info" lines
    def handle_info(self, line_data):
        # Get the info type
        info_type = line_data[1]
        # Get the value of the info row
        info_value = line_data[2]

        # If/elif/else block to determine how that information is stored
        if info_type == "visteam":
            self.current_game.set_away_team(info_value)
        elif info_type == "hometeam":
            self.current_game.set_home_team(info_value)
        elif info_type == "date":
            self.current_game.set_game_date(datetime.strptime(info_value, "%Y/%m/%d").date())
        elif info_type == "number":
            self.current_game.set_game_number(info_value)

    # Handles the "start" operation - defines the starting lineup
    def handle_start(self, line_data):
        # Retrieve the player information
        player_id = line_data[1]
        player_name = line_data[2]
        player_is_on_home_team = line_data[3]   # 0 is away team, 1 is home team
        player_lineup_order = line_data[4]
        player_starting_position = line_data[5]

        print(player_id)
        print(player_is_on_home_team)

        # First determine if we need to make a new line up
        if player_is_on_home_team not in self.lineups.keys():
            game_id = self.current_game.game_id
            team_id = self.current_game.home_team if player_is_on_home_team == 1 else self.current_game.away_team
            home_team = player_is_on_home_team

            print(game_id, team_id, home_team)

            self.lineups[player_is_on_home_team] = StartingLineupModel(game_id=game_id, team_id=team_id, home_team=home_team)

        # Populate the lineup with data
        # For now, that means nothing!