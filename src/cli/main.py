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

    allstars = AllstarAppearances()
    print(allstars.table_name_full)

    for row in allstars.select():
        print(row)


if __name__ == '__main__':
    run_cli()