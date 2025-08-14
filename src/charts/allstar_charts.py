from datetime import date, datetime
import matplotlib.pyplot as plt
import mplcursors
import numpy as np

# Data APIs
from api import allstars_api

# DB Models
from db.models.People import People
from db.models.AllstarApperances import AllstarAppearances

def top_n_allstars(limit: int = 10):
    """
    Provides the top N allstars, by number of appearances.
    Displays as a bar chart
    """
    results = allstars_api.top_n_appearances(limit)

    # Seperate out lists of players and appearances
    names = [f"{player.nameFirst} {player.nameLast}" for player in results]
    values = [player.appearances for player in results]

    # Create bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(names, values, color='skyblue')

    # Add labels and title
    plt.xlabel("Names")
    plt.ylabel("Values")
    plt.title("Bar Chart of Named Values")
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    plt.show()

def top_n_allstar_subs(limit: int = 10):
    """
    Provides the top N allstars, by number of subsitute appearances.
    Displays as a bar chart.
    """

    results = allstars_api.top_n_sub_appearances(limit)

    # Seperate out lists of players and appearances
    names = [f"{player.nameFirst} {player.nameLast}" for player in results]
    values = [player.subAppearances for player in results]

    # Create bar chart
    plt.figure(figsize=(10, 6))
    plt.bar(names, values, color='skyblue')

    # Add labels and title
    plt.xlabel("Names")
    plt.ylabel("Values")
    plt.title("Bar Chart of Named Values")
    plt.xticks(rotation=45)

    # Show the plot
    plt.tight_layout()
    plt.show()

def career_length_vs_allstar_appearances():
    """
    Displays a scatterplot of career length in years (X-axis) vs. number of allstar appearances (Y-axis).
    """
    # Establish our query:
    #   Get all players' IDs, start/end dates, and number of allstar appearances
    results = allstars_api.allstars_career_debuts_and_finales()

    # Lists to hold the plot values
    x_vals = []
    y_vals = []
    colors = []
    names  = []
    
    # Map True/False to colors
    color_map = {True: "orange", False: "blue"}

    # Get the results
    for player in results:

        # Build the information for the player:
        allstar_information = {}

        # Parse total career length
        debut = datetime.strptime(player.debut, "%Y-%m-%d").date()
        # Set final date if the player is no longer playing
        if player.finalGame is not None:
            finale = datetime.strptime(player.finalGame, "%Y-%m-%d").date()
            allstar_information["still_active"] = False
        else:
            finale = date.today()
            allstar_information["still_active"] = True

        # Add career length as x axis
        x_vals.append(((finale - debut).days) / 365.25)
        
        # Add allstar_appearances as y axis
        y_vals.append(player.allstar_appearances)

        # Setup the active/inactive player display
        colors.append(color_map[player.finalGame is None])     # No final game = True, so they're still active

        # Add the player name for a tooltip hover
        names.append(player.nameFirst + " " + player.nameLast)
    

    # Create scatter plot
    scatter = plt.scatter(x_vals, y_vals, c=colors, edgecolor="black")

    # Labels and title
    plt.xlabel("Career Length")
    plt.ylabel("Number of Appearances")
    plt.title("Career Length vs. Appearances")
    plt.grid(True)

    # Add hover tooltips
    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_hover(sel):
        idx = sel.index
        sel.annotation.set_text(names[idx])

    plt.show()