# Native libraries
import argparse
import os
import sys

# My Modules
from db.models.AllstarApperances import AllstarAppearances
from db.models.People import People
from charts import allstar_charts

def run_cli():
    
    print("Starting main function...")

    ###
    #
    # Testing queries below
    #
    ###

    allstar_charts.top_ten_allstar_subs()



if __name__ == '__main__':
    run_cli()