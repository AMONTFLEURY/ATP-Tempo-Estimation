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

    if not UDManager.check_for_index(songList[index]):
        vector, y, sr = (TempoEstimator.getTempoVector(pathList[index]))
        print(vector)
        new = [index, songList[index], vector]
        loaded_songs.append(new)
        UDManager.add_row(loaded_songs[-1])
        return vector


def getAllVectors(cores):
    with Pool(cores) as p:
        for result in p.imap(TempoEstimator.getTempoVector, pathList):
            frame.append(result[0])
            print(len(frame), "out of", len(songList))
            print(result[0])
    for i in frame:
        print(i)

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
    1. Get All Tempos
    2. Get One Tempo vector
    3. List of all songs
    4.View table
    5. Get loaded songs
    6. Verify Files 
    7. Save User Data
    """)
        if choice == "1":
            cores = input(f"Number of cores (1 - {SystemManager.getCPUcount()}):")
            getAllVectors(int(cores))
        elif choice == '2':
            index = input("index:")
            getVector(int(index))
        elif choice == '3':
            getSongList()
        elif choice == '4':
            RefTableManager.view_reference_table()
        elif choice == '5':
            getLoaded()
        elif choice == '6':
            SystemManager.checkFiles()
        elif choice == '7':
            UDManager.saveTable()
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

    Interface()

    print(f"Time elapsed: {end - start} seconds")

    # print(TempoEstimator.DynamicTempoAlgo(pathList[2]))
    # print(TempoGetter.get_Dtempo(pathList[2], sr_multiplier= 4, starting_tempo= 160))
    # TempoEstimator.combinedAlgo(pathList)
