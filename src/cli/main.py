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

    sql = AllstarAppearances.select().aggregate(count=[{"yearCol":"*"}]).group_by("yearID").build_query()
    print(sql)
    

    # for player in People.allstar_apperances():
    #     print(player.playerID + " - " + player.nameFirst + " " + player.nameLast + " - " + str(player.appearances))


if __name__ == '__main__':
    run_cli()