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
    query2 = Query(People)

    # Empty select
    query2 = query2.select().join(AllstarAppearances, "playerID")

    print(query2.build_query())

    query = (People.select(f"{People.table_name_full()}.playerID", "nameFirst", "nameLast")
                   .aggregate(count=[{"allstar_appearances": "*"}])
                   .join(AllstarAppearances, "playerID")
                   .group_by(f"{People.table_name_full()}.playerID", "nameFirst", "nameLast")
                   .having(count=[{">": 20}]))

    for player in query.execute():
        print(f"{player.nameFirst} {player.nameLast} -- {player.allstar_appearances}")



if __name__ == '__main__':
    run_cli()