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

    for player in AllstarAppearances.select().aggregate(count=[{"playerCount":"*"}]).group_by("yearID").order_by(yearID="DESC").execute():
        print(player)



if __name__ == '__main__':
    run_cli()