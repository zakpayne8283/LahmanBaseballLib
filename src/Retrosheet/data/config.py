# Data folder(s)
base_directory = "_data/_downloads/"
zips_directory = "_zips/"
eves_directory = "_eves/"

# Retrosheet Play-By-Play Data URL to download from, depending on the year
plays_zip_name_base = "[YEAR]plays.zip"
plays_csv_name_base = "[YEAR]plays.csv"
plays_base_download_url = "https://www.retrosheet.org/downloads/plays/[FILE_NAME]"

# Retrosheet Events Data URL to download from
events_zip_name_base = "[YEAR]eve.zip"
events_base_download_url = "https://www.retrosheet.org/events/[FILE_NAME]"

# Retrosheet Derived Database Information
retrosheet_database_name = "retrosheet_data"

# Bounds for which years to download
min_year = 2024 # TODO: Up this - starting with this for testing
max_year = 2024 # TODO: Maybe find a way to make this programmatically? Retrosheet updates data yearly though