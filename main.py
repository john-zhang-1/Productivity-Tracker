import datetime
from os import path
import numpy as np
import matplotlib.pyplot as plt


def initialize(date, rewards_doc):
    """Runs main program loop that allows functions to be used as user inputs"""

    while True:
        print("Possible Actions:\n")
        print("1 - Record")
        print("2 - View")
        print("3 - Graph")
        print("4 - Organize")
        print("Press any other key to close")
        print("")
        action = input("Action\n")

        if action == "1": # record
            # Receives user inputs relating to activity data and stores them in variables 'activity' and 'time_spent'
            print("Enter activity details\n")
            activity = input("Activity - ")
            time_spent = int(input("Time Spent (minutes) - "))

            # records activity data in daily document
            record_activity(activity, time_spent, date)

        elif action == "2": # view
            view_activities(date)

        elif action == "3": # graph
            graph_activities(date)

        elif action == "4": # organize
            organize_document(date)

        else: # close
            break

        print("\n")


def get_datetime():
    """Returns the time"""
    time = datetime.datetime.now()
    return time


def convert_datetime_to_valid_date(date):
    """Given a date by datetime.datetime.now(), convert it into a valid name for txt files"""
    date = date.strftime("%x") + ".txt"
    date = date.replace("/", "-")
    return date


def get_time(date):
    """Given datetime by datetime.datetime.now() returns time"""
    return date.strftime("%X")


def print_date(date):
    """Given a date, print out the following message"""
    print("Today's date: " + date)


def record_activity(activity, time_spent, filename):
    """given an activity, time spent on activity, and the date in file name format,
    records the activity information on the file 'filename.txt'"""
    print_date(filename)

    # checks whether the file already exists or not, if not, creates a new file
    if path.exists(filename):
        f = open(filename, "a")
    else:
        f = open(filename, "w")

    # finds current time
    time = get_time(get_datetime())

    # records the activity and time spent with the time when the activity was completed
    f.write(time + ": " + activity + ": " + str(time_spent))
    f.close()

    # updates reward point document
    update_reward_points(None, time_spent, time, rewards_doc)


def view_activities(filename):
    """prints the files' activities if the file exists"""
    print_date(filename)

    # checks whether the day's file exists, then prints files' contents if it does
    if path.exists(filename):
        f = open(filename)
        text = f.read()
        f.close()
        print(text)

    # if not, prints a message
    else:
        print("No recorded activities today")


def graph_activities(filename):
    """graphs the daily activities and times spent as a bar graph using data from a file"""

    f = open(filename)
    lines = f.readlines()

    # creates lists of activities and times to use for graphing
    activities = []
    times = []

    # adds activities and times into lists from the file
    for line in lines:
        line = line.replace("\n", "")
        columns = line.split(": ")
        activities.append(columns[1])
        times.append(int(columns[2]))
    f.close()

    # creates and displays graph
    index = np.arange(len(activities))
    plt.bar(index, times)
    plt.xlabel('Activity', fontsize=10)
    plt.ylabel('Time Spent', fontsize=10)
    plt.xticks(index, activities, fontsize=8, rotation=30)
    plt.title(filename)
    plt.show()


def organize_document(filename):
    """given a file with various activities and times,
    combine all instances of the same activity together and add all times up"""
    f = open(filename)
    lines = f.readlines()

    dict = {}

    for line in lines:
        line = line.replace("\n", "")
        columns = line.split(": ")
        # adds activities as keys in a dictionary, or if the key already exists, add the time onto the value of that key
        if columns[1] in dict:
            dict[columns[1]] += int(columns[2])
        else:
            dict[columns[1]] = int(columns[2])
    f.close()

    # writes the dictionary on the document now with activities' times collected
    new = open(filename, "w")
    time = get_time(get_datetime())

    for key in dict:
        new.write(time + ": " + key + ": " + str(dict[key]) + "\n")
    new.close()

    print_date(filename)
    print("Successfully organized")


def update_reward_points(activity_type, time_spent, time, rewards_doc):
    """changes the rewards document values based on activity data"""
    f = open(rewards_doc)
    f_lines = f.readlines()

    # stores all information of the text file temporarily before being updated
    dict = {}
    for line in f_lines:
        line = line.replace("\n", "")
        columns = line.split(": ")
        dict[columns[0]] = int(columns[1])
    f.close()

    # Adds points based on time spent to temporary data
    dict["Experience"] += time_spent * 50
    dict["Luxury Points"] += (time_spent // 4) ** 2

    if int(time[0:2]) >= 22 or int(time[0:2]) <= 6:
        dict["Health"] -= time_spent * 10

    else:
        dict["Health"] += time_spent * 30

    # reopens rewards document and rewrites temporary data
    new = open(rewards_doc, "w")
    for key in dict:
        new.write(key + ": " + str(dict[key]) + "\n")
    new.close()


def create_awards_file():
    """Creates the rewards file and sets it up"""

    pass


# TODO: Add different categories of activities as choices before activity name is entered as an input
#   Calculate rewards based on this
#   Add reward prizes purchased with points and different trophies for xp gained in a day, motivation, etc.
#   Penalize for spending too much time in bad categories
#
# TODO: Separate daily documents into two parts,
#   one that tracks the total times of different activities sorted into categories,
#   one that is a time log of activities
#   Use the part with total times of different activities to graph, with different bar colours for different categories
#   Calculate a daily productivity rating and other statistics
#   Store daily statistics on a calendar or document that has every day

# TODO: create calendar which shows activities done in a day

# TODO: improve simplistic rewards system to subtract points based on time spent in sleeping hours


if __name__ == "__main__":
    date = convert_datetime_to_valid_date(get_datetime())
    print_date(date)
    rewards_doc = "Rewards.txt"
    initialize(date, rewards_doc)
