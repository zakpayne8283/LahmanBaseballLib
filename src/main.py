# Native libraries
import argparse
import os
import sys

# My Modules
from charts import allstar_charts

def run_cli():
    
    print("Starting main function...")

    ###
    #
    # Testing queries below
    #
    ###
    # allstar_charts.career_length_vs_allstar_appearances()
    allstar_charts.allstar_appearances_per_opportunity()


if __name__ == '__main__':
    run_cli()