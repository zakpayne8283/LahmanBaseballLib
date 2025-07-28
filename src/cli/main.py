# Native libraries
import argparse
import os
import sys

# My Modules
from db.models.AllstarApperances import AllstarAppearances
from db.models.People import People

def run_cli():
    
    print("Starting main function...")

    ###
    #
    # Testing queries below
    #
    ###

    # AllstarAppearances.select().where(yearID=2000).execute()

    for player in People.select().where(birthYear="1979").execute():
        print(player.playerID + " - " + player.nameFirst + " " + player.nameLast)


if __name__ == '__main__':
    run_cli()