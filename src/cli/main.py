# Native libraries
import argparse
import os
import sys

# My Modules
from db.models.AllstarApperances import AllstarAppearances
from db.models.People import People
from db.models.query_builder import Query
from charts import allstar_charts

def run_cli():
    
    print("Starting main function...")

    ###
    #
    # Testing queries below
    #
    ###
    query = People.select("playerID", "nameFirst", "nameLast").where(playerID=AllstarAppearances.select("playerID").where(yearID=2024))

    for player in query.execute():
        print(player.nameFirst + " " + player.nameLast)



if __name__ == '__main__':
    run_cli()