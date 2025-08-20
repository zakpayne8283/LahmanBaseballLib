import os
import requests # type: ignore
import zipfile

import Retrosheet.data.config as retrosheet_configs

def download_and_extract_retrosheet_data():
    """
    As needed, downloads and extracts data into the data folder for all retrosheet play-by-play data
    """
    # Create the download/extract directories, as needed.
    _setup_directory_structure()

    # For each year we're downloading,
    for year in range(retrosheet_configs.min_year, retrosheet_configs.max_year + 1):  # +1 here because range() is exclusive
        print(f"Setting up data for year: {year}")

        # Download data (if needed)
        _download_retrosheet_data(year)

        # Extract csv file (if needed)
        _extract_retrosheet_data(year)

        print(f"Finished retrieving/extracting data for year: {year}")

def _download_retrosheet_data(year: int):
    """
    Downloads the event data for the specified year
    """
    # Where we expect our zip files to be
    zip_folder = os.path.join(retrosheet_configs.base_directory, retrosheet_configs.zips_directory)

    # The zip_folder directory should exist, but nice to check anyway
    if not os.path.exists(zip_folder):
        raise Exception("BASE DIRECTORY NOT FOUND - Ensure setup is being run correctly.")

    # Set the expected file name
    file_name = retrosheet_configs.events_zip_name_base.replace("[YEAR]", str(year))

    # Check if we already have the zip data
    target_file = os.path.join(zip_folder, file_name)

    # If not, download it
    if not os.path.exists(target_file):
        # Set target URL
        target_url = retrosheet_configs.events_base_download_url.replace("[FILE_NAME]", file_name)

        print(f"Beginning download from {target_url}...")

        # Download the file
        download_response = requests.get(target_url)
        download_response.raise_for_status()

        # Save the file
        with open(target_file, "wb") as f:
            f.write(download_response.content)

        print(f"Saved download to ({target_file})")
    else:
        print(f"File ({target_file}) already exists - skipping download...")

def _extract_retrosheet_data(year: int):
    """
    Extracts the downloaded zip files into their usable CSV files
    """
    # Where we expect our CSV files to be
    eve_folder = os.path.join(retrosheet_configs.base_directory, retrosheet_configs.eves_directory)

    # The csv_folder directory should exist, but nice to check anyway
    if not os.path.exists(eve_folder):
        raise Exception("BASE DIRECTORY NOT FOUND - Ensure setup is being run correctly.")

    # Set the expected zip folder's path
    expected_zip_folder = os.path.join(retrosheet_configs.base_directory, retrosheet_configs.zips_directory, retrosheet_configs.events_zip_name_base.replace("[YEAR]", str(year)))

    # Extract from the ZIP to the csv folder
    print(f"Extracting Event files from {expected_zip_folder}...")
    with zipfile.ZipFile(expected_zip_folder, "r") as zip_file:
        # For each file in the zip file
        for event_file in zip_file.namelist():
            # Get the expected file path
            event_file_path = os.path.join(retrosheet_configs.base_directory, retrosheet_configs.eves_directory, event_file)
            # If the file doesn't already exist, extract it
            if not os.path.exists(event_file_path) and (event_file.endswith(".EVN") or event_file.endswith(".EVA")):
                zip_file.extract(event_file, os.path.join(retrosheet_configs.base_directory, retrosheet_configs.eves_directory))
                print(f"Extracted: {event_file}")
            else:
                print(f"Skipping file: {event_file}")
        

def _setup_directory_structure():
    """
    Defines the expected directory structure
    """
    # Create the base directory for all data first
    if not os.path.exists(retrosheet_configs.base_directory):
        os.makedirs(retrosheet_configs.base_directory, exist_ok=True)
        print(f"Created data root directory: {retrosheet_configs.base_directory}!")
    else:
        print(f"Root directory (./{retrosheet_configs.base_directory}) already exists - skipping...")

    # Create the folder for our zip files
    zip_folder = os.path.join(retrosheet_configs.base_directory, retrosheet_configs.zips_directory)
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder, exist_ok=True)
        print(f"Created zip files directory: {zip_folder}!")
    else:
        print(f"Zip directory (./{zip_folder}) already exists - skipping...")

    # Create the folder for the csv files
    eve_folder = os.path.join(retrosheet_configs.base_directory, retrosheet_configs.eves_directory)
    if not os.path.exists(eve_folder):
        os.makedirs(eve_folder, exist_ok=True)
        print(f"Created event files directory: {eve_folder}!")
    else:
        print(f"Events directory (./{eve_folder}) already exists - skipping...")

    print("-------------------------")
