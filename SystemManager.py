import os
import multiprocessing

songPaths = []


def pullPaths():
    fileScanner = os.scandir("Music")
    for files in fileScanner:
        fileName = files
        songPaths.append("Music/" + (fileName.__str__())[11:-2])
        print((fileName.__str__())[11:-2])
    return songPaths


def getCPUcount():
    return os.cpu_count()


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
