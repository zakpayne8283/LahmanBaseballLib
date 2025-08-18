import os
import requests # type: ignore
import zipfile

# Data folder(s)
base_directory = "_data/_downloads/"
zips_directory = "_zips/"
csvs_directory = "_csvs/"

# Retrosheet URL to download from, depending on the year
zip_name_base = "[YEAR]plays.zip"
csv_name_base = "[YEAR]plays.csv"
base_download_url = "https://www.retrosheet.org/downloads/plays/[FILE_NAME]"

# Bounds for which years to download
min_year = 2024 # TODO: Up this - starting with this for testing
max_year = 2024 # TODO: Maybe find a way to make this programmatically? Retrosheet updates data yearly though

def populate_retrosheet_data():
    """
    As needed, downloads and extracts data into the data folder for all retrosheet play-by-play data
    """

    # Create the download/extract directories, as needed.
    _setup_directory_structure()

    # For each year we're downloading,
    for year in range(min_year, max_year + 1):  # +1 here because range() is exclusive
        print(f"Setting up data for year: {year}")

        # Download data (if needed)
        _download_retrosheet_data(year)

        # Extract csv file (if needed)
        _extract_retrosheet_data(year)

        print(f"Finished setting up data for year: {year}")

    print(f"Finished populating retrosheet data!")


def _download_retrosheet_data(year: int):
    """
    Downloads the play-by-play data for the specified year
    """
    # Where we expect our zip files to be
    zip_folder = os.path.join(base_directory, zips_directory)

    # The zip_folder directory should exist, but nice to check anyway
    if not os.path.exists(zip_folder):
        raise Exception("BASE DIRECTORY NOT FOUND - Ensure setup is being run correctly.")

    # Set the expected file name
    file_name = zip_name_base.replace("[YEAR]", str(year))

    # Check if we already have the zip data
    target_file = os.path.join(zip_folder, file_name)

    # If not, download it
    if not os.path.exists(target_file):
        # Set target URL
        target_url = base_download_url.replace("[FILE_NAME]", file_name)

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
    csv_folder = os.path.join(base_directory, csvs_directory)

    # The csv_folder directory should exist, but nice to check anyway
    if not os.path.exists(csv_folder):
        raise Exception("BASE DIRECTORY NOT FOUND - Ensure setup is being run correctly.")

    # Set the expected file name
    file_name = csv_name_base.replace("[YEAR]", str(year))

    # Check if we already have the CSV data
    target_file = os.path.join(csv_folder, file_name)

    if not os.path.exists(target_file):
        # Extract the zip file and save the CSV in the folder

        # Set the expected zip folder's path
        expected_zip_folder = os.path.join(base_directory, zips_directory, zip_name_base.replace("[YEAR]", str(year)))

        # Extract from the ZIP to the csv folder
        print(f"Extracting CSV ({file_name}) from {expected_zip_folder}...")
        with zipfile.ZipFile(expected_zip_folder, "r") as z:
            z.extractall(csv_folder)
        
        print(f"File ({file_name}) extracted successfully...")
    else:
        print(f"CSV file ({target_file}) already exists - skipping...")

def _setup_directory_structure():
    """
    Defines the expected directory structure
    """
    # Create the base directory for all data first
    if not os.path.exists(base_directory):
        os.makedirs(base_directory, exist_ok=True)
        print(f"Created data root directory: {base_directory}!")
    else:
        print(f"Root directory (./{base_directory}) already exists - skipping...")

    # Create the folder for our zip files
    zip_folder = os.path.join(base_directory, zips_directory)
    if not os.path.exists(zip_folder):
        os.makedirs(zip_folder, exist_ok=True)
        print(f"Created zip files directory: {zip_folder}!")
    else:
        print(f"Zip directory (./{zip_folder}) already exists - skipping...")

    # Create the folder for the csv files
    csv_folder = os.path.join(base_directory, csvs_directory)
    if not os.path.exists(csv_folder):
        os.makedirs(csv_folder, exist_ok=True)
        print(f"Created zip files directory: {csv_folder}!")
    else:
        print(f"CSV directory (./{csv_folder}) already exists - skipping...")

    print("-------------------------")
