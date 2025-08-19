import os
import pyodbc

# Retrosheet data stuff
import Retrosheet.data.config as retrosheet_configs
from Retrosheet.data.models.retrosheet_table import RetrosheetTable

# Data Models
from Retrosheet.data.models.Game import Game as GameModel

def generate_database_from_event_files():
    # Setup the database first
    establish_retrosheet_database()
    # Create the base tables in the database
    establish_retrosheet_database_tables()

    # Get the folder where the event files are
    events_folder = os.path.join(retrosheet_configs.base_directory, retrosheet_configs.eves_directory)

    # For each file in the events folder,
    for event_file in os.listdir(events_folder):

        # Build the file path
        event_file_path = os.path.join(events_folder, event_file)

        if os.path.isfile(event_file_path):  # skip subdirectories

            print(f"Found file: ({event_file_path}) - parsing...")

            parse_event_file(event_file_path)

            print(f"Finished parsing file ({event_file_path})!")

def establish_retrosheet_database():
    # Establish the connection
    db_connection = RetrosheetTable.get_connection(enable_autocommit=True)
    # Get the cursor
    cursor = db_connection.cursor()
    # Set the DB name
    db_name = retrosheet_configs.retrosheet_database_name

    print(f"Checking if database {db_name} exists...")

    # Check if the DB exists
    cursor.execute("SELECT database_id FROM sys.databases WHERE name = ?", db_name)
    row = cursor.fetchone()

    # If it exists, delete it
    if row:
        print(f"Database '{db_name}' already exists...")
    else:
        # Create the database
        print(f"Creating database '{db_name}'...")
        cursor.execute(f"CREATE DATABASE [{db_name}]")
        db_connection.commit()

def establish_retrosheet_database_tables():
    # Get our models for creation
    GameModel.create_table()

def parse_event_file(file_path):
    # Open the event file
    with open(file_path, "r") as event_file:

        # The current game we're building stats for
        current_game = None

        # Process each line
        for line in event_file:
            # Strip and split the data
            line_data = line.strip().split(",")

            operation = line_data[0]    # id, start, play, sub, etc.

            if operation == "id":
                """
                    Example Data:
                    id,ANA202404050

                    This data is consistent, and will always follow this format. 
                """
                
                # New game starting, take action accordingly
                if current_game is not None:
                    # Flush the current game
                    current_game.insert_into_db()
                
                # Get the game ID
                game_id = line_data[1]

                # Create a new game object
                current_game = GameModel(game_id=game_id)
            elif operation == "info":
                """
                    EXAMPLE DATA:
                    info,visteam,BOS
                    info,hometeam,ANA
                    info,site,ANA01
                    info,date,2024/04/05
                """

                info_type = line_data[1]

                if info_type == "visteam":
                    current_game.set_away_team(line_data[2])
                elif info_type == "hometeam":
                    current_game.set_home_team(line_data[2])
            
    