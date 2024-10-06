import os
import csv

import matplotlib.pyplot as plt
import matplotlib.lines as mlines

from ast import literal_eval

# Read the data into a list using literal_eval
# Returns a list of filenames along with a list of those files' commits

def get_list_from_csv(filename: str) -> list:

    output = []

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                output.append([row["Filename"], literal_eval(row["Touches"])])
            except:
                print("Error when parsing filename " + row["Filename"])
    
    return output

# Give each author their own color
# Returns author colors, author commit counter, and total author counter

def get_author_data(commitData: list):

    authorColors = dict()

    colorItems = [
        "aqua", "darkcyan", "indigo", "blue", "blueviolet",
        "brown", "coral", "crimson", "gray", "darkgreen",
        "darkorange", "gold", "lightpink", "lime", "olive",
        "lightslategray", "lightsteelblue", "peru", "royalblue", "pink",
        "tan", "teal", "tomato", "violet", "yellow",
        "darkorchid", "darkred", "darksalmon", "deeppink", "darkslateblue",
        "goldenrod", "khaki", "lightseagreen", "mediumblue", "mediumaquamarine",
        "mediumseagreen", "mediumslateblue", "mediumvioletred", "midnightblue", "navajowhite",
        "olivedrab", "orangered", "orchid", "purple", "saddlebrown",
        "salmon", "sienna", "seagreen", "skyblue", "silver"
    ]

    # Counts the total amount of authors
    authorCounter = 0

    # Counts how many commits each author makes
    authorCommitCounter = dict()

    for row in commitData:
        for individualCommit in row[1]:
            # Increment author commit counter
            authorCommitCounter[individualCommit[0]] = authorCommitCounter.get(individualCommit[0], 0) + 1

            # Give the author a color if they don't have a color
            if individualCommit[0] not in authorColors:
                if authorCounter >= len(colorItems):
                    authorColors[individualCommit[0]] = "black"
                    print(individualCommit[0], "was assigned 'black' by default. More colors are needed.")
                else:
                    authorColors[individualCommit[0]] = colorItems[authorCounter]

                authorCounter += 1
    
    return authorColors, authorCommitCounter, authorCounter


# Translate dates into weeks

def date_to_weeks(date: str) -> float:
    
    # Extract years

    delimitIndex = date.find('-')
    
    if delimitIndex == -1:
        return -1
    
    # Convert years to days and subtract a constant
    output = 365 * (float(date[:delimitIndex]) - 1950)

    date = date[delimitIndex+1:]

    # Extract months

    delimitIndex = date.find('-')

    if delimitIndex == -1:
        return -2

    output += float(date[:delimitIndex]) * 30.5

    date = date[delimitIndex+1:]

    # Extract days

    delimitIndex = date.find('T')

    if delimitIndex == -1:
        return -3
    
    output += float(date[:delimitIndex])

    return output / 7.0

# Get the earliest week to subtract from other dates

def get_earliest_week(commitData: list) -> float:

    earliestWeek = date_to_weeks(commitData[len(commitData) - 1][1][0][1]) # Initialize the earliest week with the first found date

    for file in commitData:
        for commit in file[1]:
            thisWeek = date_to_weeks(commit[1])

            if thisWeek < earliestWeek:
                earliestWeek = thisWeek
    
    return earliestWeek


# Takes a dict of authors and their commit counter
# Returns an ordered list of those authors with more commits
# occurring earlier in the list


def get_author_commit_counter_list(authorCommitCounter: dict) -> list:
    # Convert the dictionary to a list of tuples and sort by commit counts in descending order
    authorCommitCounterList = sorted(authorCommitCounter.items(), key=lambda x: x[1], reverse=True)
    
    return authorCommitCounterList


# Main block where driving code is


if __name__ == "__main__":

    dataFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "authorsFileTouches_file_rootbeer.csv")

    commitData = get_list_from_csv(dataFile)

    authorColors, authorCommitCounter, authorCounter = get_author_data(commitData)

    earliestWeek = get_earliest_week(commitData)

    authorCommitCounterList = get_author_commit_counter_list(authorCommitCounter)
        
    x = []
    y = []
    colors = []
 
    # Translates the data into three lists to plot on a scatterplot
    for index, file in enumerate(commitData):
        for commit in file[1]:
            
            # Adds the file index to the x list
            x.append(index)

            # Adds the date difference to the y list
            y.append(date_to_weeks(commit[1]) - earliestWeek)

            # Adds the color to the c list
            colors.append(authorColors[commit[0]])

    fig, ax = plt.subplots()

    scatter = plt.scatter(x, y, c=colors, s=25)

    plt.xlabel("File")
    plt.ylabel("Week")

    # Make the legend

    markers = []

    for author in authorCommitCounterList:
        markers.append(mlines.Line2D([], [], color=authorColors[author[0]], marker='o', markersize=10, linestyle="None", label=f"{author[0]} ({authorCommitCounter[author[0]]})"))

    legend = ax.legend(handles=markers, bbox_to_anchor=(1, 1), fontsize=9)

    ax.add_artist(legend)

    # Save the scatterplot as "Commits.png", then show it

    plt.savefig("Commits", bbox_extra_artists=(legend,), bbox_inches="tight")
    plt.show()
