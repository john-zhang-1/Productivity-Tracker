import datetime
import time
from os import path
import os
import random
import numpy as np
import matplotlib.pyplot as plt

def activity_track(date, rewards_doc):
    global schedule

    schedule = {}
    date = date.strftime("%x")
    filename = str(date) + ".txt"
    filename = filename.replace("/", "-")

    while True:
        print("Possible Actions:\n")
        print("1 - Record")
        print("2 - Motivate")
        print("3 - Save")
        print("4 - View")
        print("5 - Moderate")
        print("6 - Graph")
        print("7 - Organize")
        print("8 - Close")
        print("")
        action = (input("Action\n")).lower()

        if action == "1":
            print("Enter activity details\n")

            activity = input("Activity - ")

            if activity in schedule:
                print("Today: " + str(schedule[activity]) + " minutes")
            else:
                print("Today: " + "0 minutes" )

            time_spent = int(input("Time Spent (minutes) - "))

            if activity not in schedule:

                schedule[activity] = time_spent

            else:
                schedule[activity] += time_spent

            f2 = open(rewards_doc)
            f2_lines = f2.readlines()

            dict = {}

            for line in f2_lines:
                line = line.replace("\n", "")
                columns = line.split(": ")

                dict[columns[0]] = int(columns[1])

            f2.close()

            dict["Experience"] += time_spent * 50
            dict["Luxury Points"] += (time_spent//4) ** 2
            dict["Health"] += time_spent * 10

            new = open(rewards_doc, "w")
            for key in dict:
                new.write(key + ": " + str(dict[key]) + "\n")
            new.close()

            for i in schedule:
                print(i.upper() + ": " + str(schedule[i]))
            print("\n")

        elif action == "2":
            print("John. Think it through. You NEED TO STOP AND JUST STUDY! DO IT FOR YOUR FUTURE")
            print("NOW GET OFF WHATEVER YOU'RE DOING. THINK ABOUT IT LONG TERM. THINK ABOUT HOW AWFUL IT FEELS AFTER WASTING YOUR TIME")

        elif action == "3":

            print("Today's date': " + filename)

            if path.exists(filename):
                f = open(filename, "a")
            else:
                f = open(filename, "w")
            t = datetime.datetime.now()
            for key in schedule:
                f.write(t.strftime("%X") + ": " + key + ": " + str(schedule[key]) + "\n")

            f.close()
            f = open(filename)
            text = f.read()
            f.close()
            print(text)

        elif action == "4":
            if path.exists(filename):
                print("Today's date': " + filename)
                f = open(filename)
                text = f.read()
                f.close()
                print(text)
            else:
                print("No recorded activities today")

        elif action == "5":
            t = (float(input("Time (minutes) - ")) * 60)
            initial = time.time()
            final = initial + int(t)
            while time.time() < final:
                print("Moderating...")
                time.sleep(random.random() * 10)
                print("Think about what you're doing right now")
                time.sleep(random.random() * 10)
            print("Time's Up!")

        elif action == "6":

            f = open(filename)
            lines = f.readlines()

            activities = []
            times = []

            for line in lines:
                line = line.replace("\n", "")
                columns = line.split(": ")
                activities.append(columns[1])
                times.append(int(columns[2]))
            f.close()

            index = np.arange(len(activities))
            plt.bar(index, times)
            plt.xlabel('Activity', fontsize = 10)
            plt.ylabel('Time Spent', fontsize = 10)
            plt.xticks(index, activities, fontsize = 8, rotation = 30)
            plt.title(date)
            plt.show()

        elif action == "7":
            f = open(filename)
            lines = f.readlines()

            dict = {}

            for line in lines:
                line = line.replace("\n", "")
                columns = line.split(": ")

                if columns[1] in dict:
                    dict[columns[1]] += int(columns[2])
                else:
                    dict[columns[1]] = int(columns[2])
            f.close()

            new = open(filename, "w")
            t = datetime.datetime.now()
            for key in dict:
                new.write(t.strftime("%X") + ": " + key + ": " + str(dict[key]) + "\n")
            new.close()

        elif action == "8":
            break
        else:
            print("Invalid Action")



        print("\n")



# TODO: Add different categories of activities as choices before activity name is entered as an input
#   Calculate rewards based on this
#   Add reward prizes purchased with points and different trophies for xp gained in a day, motivation, etc.
#   Penalize for spending too much time in bad categories
#
# TODO: Separate daily documents into two parts, one that tracks the total times of different activities sorted into categories,
#   one that is a time log of activities
#   Use the part with total times of different activities to graph, with different bar colours for different categories
#   Calculate a daily productivity rating and other statistics
#   Store daily statistics on a calendar or document that has every day
#
# TODO: Have entries save automatically in the daily document on the time log and update the total times automatically,
#   remove save and organize actions
#
# TODO: create a class for a document, and make the actions methods and make local variables attributes
#


def create_awards_file():
    """Creates the rewards file and sets it up"""

    pass


if __name__ == "__main__":
    day = datetime.datetime.now()
    rewards = "Rewards.txt"
    print("Date: " + day.strftime("%x"))
    activity_track(day, rewards)