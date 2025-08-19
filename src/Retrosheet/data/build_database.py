import os
import pyodbc

import Retrosheet.data.config as retrosheet_configs
import Retrosheet.data.connector as db_connector

def generate_database_from_event_files():
    # Setup the database first
    establish_retrosheet_database()

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



    # Parse the file, and build the database from it

# TODO: Refactor this so the database connection is useable elsewhere.
# TODO: Also make it so autocommit can be toggled, so CREATE DATABASE can use it, but regular transactions cannot.
def establish_retrosheet_database():
    # Establish the connection
    db_connection = db_connector.get_connection(enable_autocommit=True)
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

def parse_event_file(file_name):
    """
    with open("data/_downloads/extracted/game.EVN", "r") as f:
    for line in f:
        # line includes the newline at the end, so strip if you don’t want it
        print(line.strip())
    """
    pass