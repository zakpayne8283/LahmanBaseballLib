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

    for person in People.select().join(AllstarAppearances, "playerID").execute():
        print(person.nameFirst + " " + person.nameLast)


if __name__ == '__main__':
    run_cli()