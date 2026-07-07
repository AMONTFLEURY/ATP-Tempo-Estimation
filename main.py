from numpy.ma.core import floor
from numpy.ma.extras import average
import time
import SystemManager
from multiprocessing import Pool
import librosa
import TempoEstimator
import TempoGetter
import ModelTrainer
import TempoTable
import pygame

pathList, songList = (SystemManager.pullPaths())
SystemManager.getCPUcount()
CPU_list = SystemManager.splitPathList(fullList=pathList, jobs=4)
# for jobs in CPU_list:
#     print(jobs)
tempoList = []


def getBeatTimeSpacing(path):
    y, sr = librosa.load(path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr)
    beat_team = librosa.frames_to_time(beats, sr=sr)


def getSongList():
    for i in songList:
        print(i)


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
    vector, y, sr = (TempoEstimator.getTempoVector(pathList[index]))
    print(vector)
    return vector


def getAllVectors(cores):
    frame = []
    with Pool(cores) as p:
        for result in p.imap(TempoEstimator.getTempoVector, pathList):
            frame.append(result[0])
            print(len(frame), "out of", len(songList))
    print(frame)
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


def Interface():
    print("CPU Core count: ", SystemManager.getCPUcount(),
          "\nSong List Length: ", len(songList))

    input("Press Enter to Start ")

    while True:
        choice = input("""
    CPU Core count: ",SystemManager.getCPUcount(),
    Song List Length: , len(songList))
    1. Get All Tempos
    2. Get One Tempo
    3. 
    """)
        if choice == "1":
            cores = input(f"Number of cores (1 - {SystemManager.getCPUcount()}):")
            getAllVectors(int(cores))
        elif choice == '2':
            index = input("index:")
            getVector(int(index))
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

    end = time.time()
    getAllVectors(8)
    Interface()

    print(f"Time elapsed: {end - start} seconds")

    # print(TempoEstimator.DynamicTempoAlgo(pathList[2]))
    # print(TempoGetter.get_Dtempo(pathList[2], sr_multiplier= 4, starting_tempo= 160))
    # TempoEstimator.combinedAlgo(pathList)
