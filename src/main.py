# Native libraries
import argparse
import os
import sys

# My Modules
from charts import allstar_charts
import Retrosheet.setup as retrosheet_setup
from Lahman.db.models.lahman_table import LahmanTable
from Lahman.db.models.AllstarApperances import AllstarAppearances

def run_cli():
    
    print("Starting main function...")

    # Setup the retrosheet data first, to ensure we have it.
    # retrosheet_setup.setup_retrosheet_data()

    query = Query(AllstarAppearances.select().as_name("allstars")).select("playerID")

    for person in query.execute():
        print(person)

if __name__ == '__main__':
    run_cli()