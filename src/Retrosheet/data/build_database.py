import os
import pyodbc

# Retrosheet data stuff
import Retrosheet.data.config as retrosheet_configs
from Retrosheet.data.models.retrosheet_table import RetrosheetTable

# Utils
from Retrosheet.data.utils.event_parser import EventParser

# Data Models
from Retrosheet.data.models.Game import Game as GameModel
from Retrosheet.data.models.StartingLineup import StartingLineup as StartingLineupModel

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
    StartingLineupModel.create_table()

def parse_event_file(file_path):
    # Setup the EventParser
    parser = EventParser(file_path=file_path)
    # Run it
    parser.parse_event_file()
            
def drop_tables_from_database():
    GameModel.drop_table()
    StartingLineupModel.drop_table()