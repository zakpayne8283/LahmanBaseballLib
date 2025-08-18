from datetime import date, datetime
import matplotlib.pyplot as plt
import mplcursors
import numpy as np

# Data APIs
from Lahman.api import allstars_api

# DB Models
from Lahman.db.models.People import People
from Lahman.db.models.AllstarApperances import AllstarAppearances

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

def overlapping_multi_time_allstars(min_number_appearances: int = 10):
    """
    Displays a horizontal bar chart of all players with N allstar appearances, ordered by debut of first game.
    X-axis is the year, Y-axis is players, ordered ascending by their debut game.
    """
    # Establish our query:
    #   Get all players' IDs, start/end dates, and number of allstar appearances
    results = allstars_api.allstars_career_debuts_and_finales()

    # Filter our results to only players with N or more appearances
    filtered_sorted_results = sorted([player for player in results if player.allstar_appearances >= min_number_appearances], key=lambda p: p.debut, reverse=True)

    # Now build the chart data
    names = []
    debuts = []
    durations = []
    appearances = []

    for player in filtered_sorted_results:
        names.append(f"{player.nameFirst} {player.nameLast}")

        debut = datetime.strptime(player.debut, "%Y-%m-%d").date()
        # Set final date if the player is no longer playing
        if player.finalGame is not None:
            finale = datetime.strptime(player.finalGame, "%Y-%m-%d").date()
        else:
            finale = date.today()

        debuts.append(debut)
        durations.append((finale - debut).days)
        appearances.append(player.allstar_appearances)

    # Create figure
    fig, ax = plt.subplots()

    # Plot bars
    bars = ax.barh(names, durations, left=debuts, height=0.5)

    # Format x-axis as dates
    ax.xaxis_date()

    # Labels
    ax.set_xlabel("Year")
    ax.set_ylabel("Player")
    ax.set_title("Career Timelines")

    # Add mplcursors tooltips
    cursor = mplcursors.cursor(bars, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        idx = sel.index
        player = filtered_sorted_results[idx]
        sel.annotation.set_text(
            f"{player.nameFirst} {player.nameLast}\nAllstar Appearances: {player.allstar_appearances}\nDebut: {player.debut}\nFinale: {player.finalGame}"
        )
        sel.annotation.get_bbox_patch().set(alpha=0.8, facecolor="lightyellow")

    plt.tight_layout()
    plt.show()

def allstar_appearances_per_opportunity():
    """
    Shows the total number of allstar appearances a player has had relative to the number of opportunities they've had
    Opportunities are occasions where the player was eligable, and had played sufficient games played to be considered
    """
    # TODO: Work on baseline sufficient games

    # Establish our query:
    #   Get all players' IDs, names, start/end dates, and number of allstar appearances
    results = allstars_api.allstars_career_debuts_and_finales(include_as_game_id=True)

    allstar_players = []
    career_lengths = []
    allstar_appearances_per_year = []

    for player in results:
        # Store the player name
        allstar_players.append(f"{player.nameFirst} {player.nameLast}")
        
        # Establish the player's career length
        debut = datetime.strptime(player.debut, "%Y-%m-%d").date()
        # Set final date if the player is no longer playing
        if player.finalGame is not None:
            finale = datetime.strptime(player.finalGame, "%Y-%m-%d").date()
        else:
            finale = datetime.strptime('2024-12-31', "%Y-%m-%d").date()

        # Calculate career length, in total years
        # TODO: Modify this to seasons played - Minnie Minoso throws this off...
        #       Use the Appearances table to do it 
        career_length = ((finale - debut).days) / 365.25
        career_lengths.append(career_length)

        # Get the total appearances per year played, rounded to 2 decimals
        allstar_appearances_per_year.append(round(player.allstar_appearances / career_length, 2))

    # Create scatter plot
    scatter = plt.scatter(career_lengths, allstar_appearances_per_year, edgecolor="black")

    # Labels and title
    plt.xlabel("Seasons Played")
    plt.ylabel("Appearances per Year")
    plt.title("ASGs per Years Played")
    plt.grid(True)

    # Add hover tooltips
    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_hover(sel):
        idx = sel.index
        sel.annotation.set_text(allstar_players[idx])

    plt.show()

def age_of_starting_position_by_year(position=1):
    """
    Shows, as a line chart, the age of the starting player at a position each year of the Allstar Game
    """
    results = allstars_api.allstars_starters_information(position)

    allstar_players = []
    game_dates = []
    game_years = []
    players_leagues = []
    ages_of_starters = []

    # Map True/False to colors
    league_colors = {"AL": "red", "NL": "blue"}

    for starter in results:
        # Store the player name
        allstar_players.append(f"{starter.nameFirst} {starter.nameLast}")

        # Store when the game happened
        game_date = _parse_asg_date_from_id(starter.gameID)
        game_years.append(starter.yearID)
        game_dates.append(game_date)

        # Calculate the age of the starter that game
        starter_age = (game_date - date(starter.birthYear, starter.birthMonth, starter.birthDay)).days
        ages_of_starters.append(round(starter_age / 365.25, 1))

        players_leagues.append(league_colors[starter.lgID])

    # Create scatter plot
    # X Axis - Game Dates
    # Y Axis - Age of the starter that game for the position
    scatter = plt.scatter(game_dates, ages_of_starters, c=players_leagues, edgecolor="black")

    # Labels and title
    plt.xlabel("ASG Date")
    plt.ylabel("Age of Starter")
    plt.title(f"Age of Position {position} ASG Starter")
    plt.grid(True)

    # Add hover tooltips
    cursor = mplcursors.cursor(scatter, hover=True)
    @cursor.connect("add")
    def on_hover(sel):
        idx = sel.index
        sel.annotation.set_text(f"{allstar_players[idx]}\nYear: {game_years[idx]}\nAge: {ages_of_starters[idx]}")

    plt.show()



def _parse_asg_date_from_id(asg_id: str):
    """
    Given the game id for an allstar game (AllstarFull.gameID), return the date the game was played
    """

    """
    NLS199007100
    NLS194707080
    """

    year = int(asg_id[3:7])
    month = int(asg_id[7:9])
    day = int(asg_id[9:11])

    return date(year, month, day)