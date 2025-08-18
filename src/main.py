# Native libraries
import argparse
import os
import sys

# My Modules
from charts import allstar_charts
import Retrosheet.setup as retrosheet_setup

def run_cli():
    
    print("Starting main function...")

    retrosheet_setup.setup_retrosheet_data()

if __name__ == '__main__':
    run_cli()