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
    x, found = UDManager.check_for_index(songList[index])
    if not found:
        vector, y, sr = (TempoEstimator.getTempoVector(pathList[index]))
        print(vector)
        new = [index, songList[index], vector]
        loaded_songs.append(new)
        UDManager.add_row(loaded_songs[-1])
    vector = UDManager.check_for_index(songList[index])
    print(vector)
    return vector


def search(name):
    for i in range(len(songList)):
        if name in songList[i]:
            print(i, ":", songList[i])


def getAllVectors(cores):
    with Pool(cores) as p:
        for result in p.imap(TempoEstimator.getTempoVector, pathList):
            frame.append(result[0])
            print(len(frame), "out of", len(songList))
            print(result[0])
    # RefTableManager.make_data(frame, songList)
    # for col in range(len(frame[0])):
    #     print("\n\ncol:", col)
    #     for row in range(len(frame)):
    #         print(frame[row][col])
    # return frame


def crossEstimate(index):
    if type(index) == int:
        print(songList[index])
        x, found = UDManager.check_for_index(songList[index])
        if not found:
            vector, message = TempoEstimator.cross_estimation(pathList[index])
            new = [index, songList[index], vector[0]]
            loaded_songs.append(new)
            UDManager.add_row(loaded_songs[-1], vector_for_data=vector)
            print(message)

        else:
            # print(UDManager.check_for_index(songList[index]))
            # x, y = UDManager.check_for_index(songList[index])
            return x.to_string()
    else:
        # print(SystemManager.get_song_name(index))
        x, found = UDManager.check_for_index(index)
        if not found:
            vector, message = TempoEstimator.cross_estimation(index)
            new = [index, index, vector[0]]
            loaded_songs.append(new)
            UDManager.add_row(loaded_songs[-1], vector_for_data=vector)
            return message
        else:
            # print(UDManager.check_for_index(songList[index]))
            # x, y = UDManager.check_for_index(songList[index])
            return x.to_string()


def crossEstimate_all(cores):
    frame1 = []
    with Pool(cores) as p:
        for result in p.imap(crossEstimate, pathList):
            frame1.append(result)
            print(len(frame1), "out of", len(songList), " Track: ", songList[len(frame1)-1] )
            # print(result[-1])
    for i in range(len(frame1)):
        print(songList[i])
        print(frame1[i], '\n')


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


def search_song():
    name = input("Song Name: ")
    RefTableManager.song_lookup(name)


def nextButton():
    input("Press Enter to Continue")
    clear_screen()


def date_management_screen():
    while True:
        choice = input(""""
    1. Save User Data
    2. Save Model Data
    3. Print User Data
    4. Print Model Data
    5. Print Training Data
    6. Back
>: """)
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


def debug_screen():
    while True:
        choice = input("""
    1. Add New Data Points
    2. Train Model
>: """)
        if choice == '1':
            # x = input("index: ")
            RefTableManager.add_datapoint()
        elif choice == '2':
            RefTableManager.create_RTable_from_list()

        else:
            break


def tempo_estimator_screen():
    while True:
        choice = input("""
1. Get all Tempo Vectors
2. Get Single Tempo Vector
3. Estimate All Tempos
4. Estimate Single Tempo
5. Test with 'UNBEATABLE'
0. Exit
>: """)
        if choice == "1":
            cores = input(f"Number of cores (1 - {SystemManager.getCPUcount()}):")
            getAllVectors(int(cores))
        elif choice == "2":
            index = input("index:")
            getVector(int(index))
            nextButton()
        elif choice == "3":
            crossEstimate_all(input("Cores?\n::"))
            nextButton()
        elif choice == "4":
            index = input("index:")
            crossEstimate(int(index))
            nextButton()
        elif choice == "5":
            index = input("index:")
            SystemManager.edit_beat_map(crossEstimate(int(index)), '')
        elif choice == "0":
            break


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    # print("\n" * 100)


def CD_screen():
    clear_screen()
    choice = input("""
Change Directory of ?:
1.  User Music
2. 'UNBEATABLE' Test Beat Map
3.  Reset
>:
""")
    choice = choice.lower()
    if choice == "1":
        path_loc = input("path to music folder\n>:")
        SystemManager.music_dir = path_loc


def Interface():
    print("CPU Core count: ", SystemManager.getCPUcount(),
          "\nSong List Length: ", len(songList))

    input("Press Enter to Start ")

    while True:
        clear_screen()
        choice = input(f"""  
CPU Core count: {SystemManager.getCPUcount()},\n
Song List Length: {len(songList)}
1. Tempo Estimator
2. Search
3. List of all songs
4. Change Dir
5. Get loaded songs
6. Verify Files 
7. Data Manager
8. Debug
>: """)
        if choice == "1":
            tempo_estimator_screen()
        elif choice == '2':
            search(input("name : "))
        elif choice == '3':
            getSongList()
        elif choice == '4':
            CD_screen()
        elif choice == '5':
            getLoaded()
        elif choice == '6':
            SystemManager.checkFiles()
        elif choice == '7':
            date_management_screen()
        elif choice == '0':
            break
        elif choice == '8':
            # index = input("index:")
            # TempoEstimator.cross_checker(getVector(int(index)))
            debug_screen()

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
    # RefTableManager.create_RTable_from_list()
    # RefTableManager.add_datapoint()
    # Work on this LATER
    # SystemManager.edit_beat_map(105, "oa")
    # getSongList()
    # Interface()

    # SystemManager.Reorder_data()
    # print(getAllVectors(12))
    # UDManager.saveTable()
    # RefTableManager.add_datapoint()
    # RefTableManager.create_RTable_from_list()
    # crossEstimate_all(10)
    (crossEstimate(16))
    # (crossEstimate(0))
    # (crossEstimate(1))
    # (crossEstimate(2))
    # (crossEstimate(-10))
    end = time.time()


    print(f"Time elapsed: {end - start} seconds")

    # print(TempoEstimator.DynamicTempoAlgo(pathList[2]))
    # print(TempoGetter.get_Dtempo(pathList[2], sr_multiplier= 4, starting_tempo= 160))
    # TempoEstimator.combinedAlgo(pathList)
