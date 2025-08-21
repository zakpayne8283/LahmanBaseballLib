from datetime import datetime

# Models
from Retrosheet.data.models.Game import Game as GameModel
from Retrosheet.data.models.StartingLineup import StartingLineup as StartingLineupModel
from Retrosheet.data.models.GamePlayEvent import GamePlayEvent as GamePlayEventModel
# Utils
from Retrosheet.data.utils.ab_results_parser import AtBatResultsParser

class EventParser:
    def __init__(self, file_path):
        # File location on disk
        self.file_path = file_path

        # Used to track game data
        self.current_game = None

        # Used when setting the lineups
        self.starting_lineups = {}

        # Used when checking the current pitcher/fielders for the at bat
        # TODO: Right now these are StartingLineup objects, maybe just look at possibly creating Lineup object?
        self.current_lineups = {}

        # Used when creating the at bats in this game
        self.game_events = []

        # Handler methods for handling certain inputs
        self.handlers = {
            "id": self.handle_id,
            "info": self.handle_info,
            "start": self.handle_start,
            "play": self.handle_play
        }

    def parse_event_file(self):
        """
        Parses the event file for this current EventParser
        """

        unrecognized_commands = {}
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
                    # Note any unrecognized commands 
                    if operation not in unrecognized_commands:
                        unrecognized_commands[operation] = 1
                    else:
                        unrecognized_commands[operation] += 1

        print("The following unrecognized operations were found:")
        for key, value in unrecognized_commands.items():
            print(f"{key} - {value} instances")
    
    # Sends all data to database
    def flush_game_to_db(self):
        # Send the current game to the DB
        self.current_game.insert_into_db()

        # Send each lineup to the DB
        for lineup in self.starting_lineups.values():
            lineup.insert_into_db()

        # Send each game event to the DB
        for game_event in self.game_events:
            game_event.insert_into_db()

        # Reset necessary data
        self.current_game = None
        self.starting_lineups = {}
        self.current_lineups = {}
        self.game_events = []

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

        # First determine if we need to make a new line up
        if player_is_on_home_team not in self.starting_lineups.keys():
            game_id = self.current_game.game_id
            team_id = self.current_game.home_team if player_is_on_home_team == '1' else self.current_game.away_team
            home_team = player_is_on_home_team

            self.starting_lineups[player_is_on_home_team] = StartingLineupModel(game_id=game_id, team_id=team_id, home_team=home_team)

        # Populate the lineup with data

        # Player's lineup order placement
        self.starting_lineups[player_is_on_home_team].set_player_in_batting_order(player_id=player_id, order_number=player_lineup_order)
        # Player's starting position
        self.starting_lineups[player_is_on_home_team].set_player_starting_position(player_id=player_id, starting_position=player_starting_position)

    def handle_play(self, line_data):
        """
        SAMPLE DATA:
        play,1,0,duraj001,00,X,6/P78S
        play,1,0,dever001,32,CBBBS,NP
        """

        if self.current_lineups == {}:
            self._set_current_lineup(0, self.starting_lineups["0"])
            self._set_current_lineup(1, self.starting_lineups["1"])

        current_inning = line_data[1]
        bottom_inning  = line_data[2]
        batter_id      = line_data[3]
        ab_last_count  = line_data[4]
        ab_pitch_seq   = line_data[5]
        ab_result      = line_data[6]

        parsed_ab_result = AtBatResultsParser(ab_result)

        # On an NP (no play), do nothing
        #   Note - This seems to only appear substitutions, or possibly timeouts?
        if parsed_ab_result.is_no_play():
            return

        # Create our GamePlayEvent based on the data we have
        game_event = GamePlayEventModel(
                        self.current_game.game_id,
                        current_inning,
                        bottom_inning,
                        batter_id,
                        self.current_lineups[0 if bottom_inning is "1" else 1].starting_p)

        self.game_events.append(game_event)

    # Set's one of the specified lineups to a newly provided lineup
    def _set_current_lineup(self, home_team, new_lineup):
        self.current_lineups[home_team] = new_lineup