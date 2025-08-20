from Retrosheet.data.models.Game import Game as GameModel

class EventParser:
    def __init__(self, file_path):
        # File location on disk
        self.file_path = file_path

        # Used to track game data
        self.current_game = None

        # Handler methods for handling certain inputs
        self.handlers = {
            "id": self.handle_id,
            "info": self.handle_info,
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
                    print(f"Unknown operation: {operation}")

    # Handles operation="id" -- start of new game
    def handle_id(self, line_data):
        # If we already have game data (not the first game we've scanned)
        # flush current to db, then carry on.
        if self.current_game:
            self.current_game.insert_into_db()

        # Get the game ID
        game_id = line_data[1]
        # Create a new game object
        self.current_game = GameModel(game_id=game_id)

    # Handles the various "info" lines
    def handle_info(self, line_data):
        # Get the info type
        info_type = line_data[1]

        # If/elif/else block to determine how that information is stored
        if info_type == "visteam":
            self.current_game.set_away_team(line_data[2])
        elif info_type == "hometeam":
            self.current_game.set_home_team(line_data[2])