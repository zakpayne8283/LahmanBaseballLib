import matplotlib.pyplot as plt
import numpy as np

from db.models.People import People

def top_ten_allstars():
    results = People.allstar_apperances(limit=10)

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