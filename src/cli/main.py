# Native libraries
import argparse
import os
import sys

# My Modules
from db.models.AllstarApperances import AllstarAppearances
from db.models.People import People

def run_cli():
    # Used for pathing
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
    
    print("Starting main function...")

    ###
    #
    # Testing queries below
    #
    ###

    for player in AllstarAppearances.select().join(People, "playerID").aggregate(count=[{"appearances": "*"}]).group_by(["playerID"]).order_by(appearances="DESC").execute():
        print(player.playerID + " - " + str(player.appearances))

    # for player in AllstarAppearances.select().group_by(["playerID"]).execute():
    #     print (player.playerID)


if __name__ == '__main__':
    run_cli()