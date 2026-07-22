from numba import none
from numpy.ma.core import floor
from numpy.ma.extras import average
import time
import SystemManager
from multiprocessing import Pool
import librosa
import TempoEstimator
import TempoGetter
import RefTableManager
import os
import TempoTable
import UDManager
import pandas as pd
pathList, songList = (SystemManager.pullPaths())
SystemManager.getCPUcount()
CPU_list = SystemManager.splitPathList(fullList=pathList, jobs=4)
# for jobs in CPU_list:
#     print(jobs)
tempoList = []
frame = []
loaded_songs = []


def getBeatTimeSpacing(path):
    y, sr = librosa.load(path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_team = librosa.frames_to_time(beats, sr=sr)


def getSongList():
    for i in range(len(songList)):
        print(i, ":", songList[i])


def getLoaded():
    # for i in loaded_songs:
    #     print(i)
    UDManager.print_UserData()

def getTemposFromString():
    nums = SystemManager.cutLetters(SystemManager.test)
    for i in nums:
        print(i)


def getAllRawTempos(cores):
    with Pool(cores) as p:
        for result in p.imap(TempoGetter.getRawTempo, pathList):
            print(result)


def getAllTempoOneset(cores):
    with Pool(cores) as p:
        for result in p.imap(TempoGetter.get_tempo_from_onset, pathList):
            print(result)


def getVector(index):
    print(songList[index])
    # UDManager.check_for_index(songList[index])
    x = UDManager.check_for_index(songList[index])
    if x == None:
        vector, y, sr = (TempoEstimator.getTempoVector(pathList[index]))
        print(vector)
        new = [index, songList[index], vector]
        loaded_songs.append(new)
        UDManager.add_row(loaded_songs[-1])
    vector = UDManager.check_for_index(songList[index])
    print(vector)
    return vector


def getAllVectors(cores):
    with Pool(cores) as p:
        for result in p.imap(TempoEstimator.getTempoVector, pathList):
            frame.append(result[0])
            # print(len(frame), "out of", len(songList))
            # print(result[0])
    for i in frame:
        print(i[1])
    print('---------------------------------------------')
    for i in frame:
        print(i[2])
    print('---------------------------------------------')

    for i in frame:
        print(i[3])
    print('---------------------------------------------')
    for i in frame:
        print(i[4])
    print('---------------------------------------------')
    for i in frame:
        print(i[5])
    print('---------------------------------------------')
    for i in frame:
        print(i[6])
    print('---------------------------------------------')
    for i in frame:
        print(i[7])
    print('---------------------------------------------')
    for i in frame:
        print(i[8])
    print('---------------------------------------------')


    return frame


def EstimateFromDTA(index):
    print(TempoEstimator.DynamicTempoAlgo(pathList[index]))


def EstimateFromDTA_All():
    for i in pathList:
        print(TempoEstimator.DynamicTempoAlgo(pathList[i]))


def getAllTemposFromDT(cores):
    with Pool(cores) as p:
        for result in p.imap(TempoEstimator.getTempoFromDynamTempoArray, pathList):
            print(result[0])


def Tempo_from_Tempo():
    for i in pathList:
        x = (TempoEstimator.getTempoFromDynamTempoArray(i))
        print(TempoGetter.estimate_Tempo_From_Tempo(mp3Path=i, tempo=x[0]))


def nextButton():
    input("Press Enter to Continue")

def date_management_screen():
    while True:
        choice = input(""""
        1. Save User Data
        2. Save Model Data
        3. Print User Data
        4. Print Model Data
        5. Print Training Data
        6. Back
        """)
        if choice == "1":
            UDManager.saveTable()
        if choice == "2":
            RefTableManager.saveTable()
        if choice == "3":
            UDManager.view_user_data()
        if choice == "4":
            RefTableManager.view_reference_table()
        if choice == "5":
            RefTableManager.view_training_data()
        if choice == "6":
            break
    nextButton()

def tempo_estimator_screen():
    while True:
        choice = input("""
        1. Get all Tempo Vectors
        2. Get Single Tempo Vector
        3. Estimate All Tempos
        4. Estimate Single Tempo
        """)
        if choice == "1":
            cores = input(f"Number of cores (1 - {SystemManager.getCPUcount()}):")
            getAllVectors(int(cores))
        if choice == "2":
            index = input("index:")
            getVector(int(index))
        if choice == "3":
            pass
        if choice == "4":
            pass
        if choice == "5":
            break





def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    # print("\n" * 100)


def Interface():
    print("CPU Core count: ", SystemManager.getCPUcount(),
          "\nSong List Length: ", len(songList))

    input("Press Enter to Start ")

    while True:
        clear_screen()
        choice = input(f"""
        
        
        
    CPU Core count: {SystemManager.getCPUcount()},\
    Song List Length: {len(songList)}
    1. Tempo Estimator
    2. -------------------
    3. List of all songs
    4. -----------------
    5. Get loaded songs
    6. Verify Files 
    7. Data Manager
    """)
        if choice == "1":
            tempo_estimator_screen()
        elif choice == '2':
            pass
        elif choice == '3':
            getSongList()
        elif choice == '4':
            pass
        elif choice == '5':
            getLoaded()
        elif choice == '6':
            SystemManager.checkFiles()
        elif choice == '7':
            date_management_screen()
        elif choice == '0':
            break
        elif choice == '8':
            index = input("index:")
            TempoEstimator.cross_checker(getVector(int(index)))
        nextButton()



if __name__ == "__main__":
    start = time.time()
    #
    # dummy = [151.9991, 99.384, 99.384, 150]
    # dummy2 = [103.3594, 105.4688, 105.4688, 105]
    # dummy1 = []
    #
    # new_data = getVector(57)
    # ModelTrainer.create_referenceTable()
    # ModelTrainer.add_referenceRow(new_data)
    # ModelTrainer.saveTable()

    # getAllVectors(16)
    end = time.time()
    RefTableManager.create_RTable_from_list()
    Interface()

    print(f"Time elapsed: {end - start} seconds")

    # print(TempoEstimator.DynamicTempoAlgo(pathList[2]))
    # print(TempoGetter.get_Dtempo(pathList[2], sr_multiplier= 4, starting_tempo= 160))
    # TempoEstimator.combinedAlgo(pathList)
