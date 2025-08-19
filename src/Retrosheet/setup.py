from Retrosheet.data.build_database import generate_database_from_event_files
from Retrosheet.data.download_data import download_and_extract_retrosheet_data

def setup_retrosheet_data(build_database=True):
    # Downloads the event file data from retrosheet and extracts it to data folders
    download_and_extract_retrosheet_data()

    # Builds the database based off of event files
    if build_database:
        generate_database_from_event_files()
