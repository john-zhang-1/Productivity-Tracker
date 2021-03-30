import matplotlib.pyplot as plt
import datetime
import time
from os import path
import numpy as np
from playsound import playsound

def initialize(date, rewards_doc):
    """Runs main program loop that allows functions to be used as user inputs"""

    while True:
        print("Possible Actions:\n")
        print("1 - Record")
        print("2 - View")
        print("3 - Graph")
        print("4 - Organize")
        print("5 - Pomodoro")
        print("Press any other key to close")
        print("")
        action = input("Action\n")

        if action == "1":  # record
            # Receives user inputs relating to activity data and stores them in variables 'activity' and 'time_spent'
            print("Enter activity details\n")
            activity = input("Activity - ")
            time_spent = int(input("Time Spent (minutes) - "))

            # records activity data in daily document
            record_activity(activity, time_spent, date, rewards_doc)

        elif action == "2":  # view
            view_activities(date)

        elif action == "3":  # graph
            graph_activities(date)

        elif action == "4":  # organize
            organize_document(date)

        elif action == "5": # pomodoro
            start_pomodoro(date)

        else:  # close
            break

        print("\n")


def get_datetime():
    """Returns the time"""
    time = datetime.datetime.now()
    return time


def convert_datetime_to_valid_date(date):
    """Given a date by datetime.datetime.now(), convert it into a valid name for txt files"""
    return date.strftime("%x").replace("/", "-") + ".txt"


def get_time(date):
    """Given datetime by datetime.datetime.now() returns time"""
    return date.strftime("%X")


def print_date(date):
    """Given a date, print out the following message"""
    print("Today's date: " + date)


def record_activity(activity, time_spent, filename, rewards_doc):
    """given an activity, time spent on activity, and the date in file name format,
    records the activity information on the file 'filename.txt'"""
    print_date(filename)

    # checks whether the file already exists or not, if not, creates a new file
    if path.exists("Activity Data/" + filename):
        f = open("Activity Data/" + filename, "a")
    else:
        f = open("Activity Data/" + filename, "w")

    # finds current time
    time = get_time(get_datetime())

    # records the activity and time spent with the time when the activity was completed
    f.write(time + ": " + activity + ": " + str(time_spent) + "\n")
    f.close()

    # updates reward point document
    update_reward_points(None, time_spent, time, rewards_doc)


def view_activities(filename):
    """prints the files' activities if the file exists"""
    print_date(filename)

    # checks whether the day's file exists, then prints files' contents if it does
    if path.exists("Activity Data/" + filename):
        f = open("Activity Data/" + filename)
        text = f.read()
        f.close()
        print(text)

    # if not, prints a message
    else:
        print("No recorded activities today")


def graph_activities(filename):
    """graphs the daily activities and times spent as a bar graph using data from a file"""
    # gets total times of activities
    totals = organize_data(filename)

    # creates and displays graph
    plot(totals.keys(), totals.values(), filename)


def plot(x, y, filename):
    """Plots the x and y values on a bar graph"""
    # creates and displays graph
    index = np.arange(len(x))
    plt.bar(index, y)
    plt.xlabel('Activity', fontsize=10)
    plt.ylabel('Time Spent', fontsize=10)
    plt.xticks(index, x, fontsize=8, rotation=30)
    plt.title(filename)
    plt.show()


def organize_data(filename):
    """Combines all instances of the same activity together and returns a dictionary with total times"""
    f = open("Activity Data/" + filename)
    lines = f.readlines()

    totals = {}

    for line in lines:
        line = line.replace("\n", "")
        columns = line.split(": ")
        # adds activities as keys in a dictionary, or if the key already exists, add the time onto the value of that key
        if columns[1] in totals:
            totals[columns[1]] += int(columns[2])
        else:
            totals[columns[1]] = int(columns[2])
    f.close()

    return totals


def organize_document(filename):
    """given a file with various activities and times,
    combine all instances of the same activity together and add all times up"""
    new_activity_times = organize_data(filename)

    # writes the dictionary on the document now with activities' times collected
    new = open("Activity Data/" + filename, "w")
    time = get_time(get_datetime())

    for key in new_activity_times:
        new.write(time + ": " + key + ": " + str(new_activity_times[key]) + "\n")
    new.close()

    print_date(filename)
    print("Successfully organized")


def start_pomodoro(filename):
    """"Starts a pomodoro timer and records activity after completion"""
    print("Enter activity\n")
    activity = input("Activity - ")
    pomodoro_time = int(input("Total time (minutes)- "))

    while pomodoro_time < 25:
        pomodoro_time = int(input("Total time must be at least 25 minutes: "))

    print("Starting timer")
    time.sleep(pomodoro_time * 50)

    record_activity(activity + " + pomodoro", int(pomodoro_time * (5/6)), filename, rewards_doc)

    print("Starting break")
#     playsound(".wav")
    time.sleep(pomodoro_time * 10 - 223)

    record_activity("pomodoro break", int(pomodoro_time * (1/6)), filename, rewards_doc)

    print("Finished")


def update_reward_points(activity_type, time_spent, time, rewards_doc):
    """changes the rewards document values based on activity data"""
    f = open(rewards_doc)
    f_lines = f.readlines()

    # stores all information of the text file temporarily before being updated
    points = {}
    for line in f_lines:
        line = line.replace("\n", "")
        columns = line.split(": ")
        points[columns[0]] = int(columns[1])
    f.close()

    # Adds points based on time spent to temporary data
    points["Experience"] += time_spent * 50
    points["Luxury Points"] += (time_spent // 4) ** 2

    if int(time[0:2]) >= 22 or int(time[0:2]) <= 6:
        points["Health"] -= time_spent * 10

    else:
        points["Health"] += time_spent * 30

    # reopens rewards document and rewrites temporary data
    new = open(rewards_doc, "w")
    for key in points:
        new.write(key + ": " + str(points[key]) + "\n")
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
