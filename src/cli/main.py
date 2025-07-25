# Native libraries
import argparse
import os
import sys

# My Modules
from db.models.AllstarApperances import AllstarAppearances

def run_cli():
    # Used for pathing
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    print("Starting main function...")

    # Displays top X Allstar Apperances - NOTE: `allstar` here is returned as an AllstarApperances instance
    for allstar in AllstarAppearances.select(yearID=1970).limit(10).execute():
        print(allstar.playerID)


if __name__ == '__main__':
    run_cli()