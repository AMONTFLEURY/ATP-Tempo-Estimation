import os
import multiprocessing

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
        print(songName)
    return songPaths, songNames


def getCPUcount():
    return os.cpu_count()


def get_average_deviation(vector):
    x =[]
    total = 0
    for i in range(len(vector)-1):
        total += (vector[i] -  vector[i+1])
        x.append(total)
    return average(x)

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
