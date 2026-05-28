import os
import multiprocessing
import pandas as pd
import statistics as stats
from numpy.ma.extras import average


def pullPaths():
    songPaths = []
    songNames = []
    fileScanner = os.scandir("Music")
    for files in fileScanner:
        fileName = files
        songPaths.append("Music/" + (fileName.__str__())[11:-2])
        songName = ((fileName.__str__())[11:-2])
        songName = songName.replace(" (SPOTISAVER)", "")
        songName = songName.replace(".mp3", "")
        songNames.append(songName)
        # print(songName)
    return songPaths, songNames


def getCPUcount():
    return os.cpu_count()


def get_average_deviation(vector):
    total = 0
    avg = average(vector)
    for num in vector:
        total += round(abs(num - avg), 4)
    return total / len(vector)


def splitPathList(fullList, jobs=-1):
    list_of_lists = []
    if jobs == -1:
        cpus = getCPUcount()
    else:
        cpus = jobs

    # creates arrays for the amount of jobs to be done
    # splitting the full list in each cpu list evenly

    for i in range(cpus):
        list_of_lists.append([])

    for i in range(len(fullList)):
        list_of_lists[i % cpus].append(fullList[i])
    return list_of_lists


def compareDynamicTempos(arr1, arr2):
    num = []
    for i in range(len(arr1)):
        if arr1[i] == arr2[i]:
            num.append(arr1[i])
    if len(num) == 0:
        return 0, 0
    else:
        x = stats.mode(num)
        return x, num.count(x)
