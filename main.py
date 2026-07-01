from numpy.ma.core import floor
from numpy.ma.extras import average
import time
import SystemManager
from multiprocessing import Pool
import librosa
import TempoEstimator
import TempoGetter
import TempoTable

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
    print(pathList[index])
    vector, y, sr = (TempoEstimator.getTempoVector(pathList[index]))
    print(vector)


def getAllVectors(cores):
    with Pool(cores) as p:
        for result in p.imap(TempoEstimator.getTempoVector, pathList):
            print(result[0][1])


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


if __name__ == "__main__":
    start = time.time()

    dummy = [151.9991, 99.384, 99.384, 150]
    dummy2 = [103.3594, 105.4688, 105.4688, 105]
    dummy1 = []
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[60])
    # print(pathList[60])
    # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # vector[3] = TempoEstimator.crossChecker(vector, dummy)
    # print(vector, '\n')

    # vector, y, sr = TempoEstimator.getTempoVector(pathList[6])
    # print(pathList[6])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[10])
    # print(pathList[10])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[30])
    # print(pathList[30])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[22])
    # print(pathList[22])
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[9])
    # print(pathList[9] )
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[109])
    # print(pathList[109] )
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    #
    # vector, y, sr = TempoEstimator.getTempoVector(pathList[118])
    # print(pathList[118] )
    # # vector[3] = TempoEstimator.DTA_checker(vector, y, sr)
    # # vector[3] = TempoEstimator.crossChecker(vector, dummy2)
    # print(vector, '\n')
    # start = time.time()
    # print(TempoEstimator.getTempoVectorMP(pathList[9]))
    # end = time.time()
    # print(f"Time elapsed: {end - start} seconds\n")

    #
    # start = time.time()
    # print(pathList[12])
    # vector, y, sr = (TempoEstimator.getTempoVector(pathList[12]))
    # print(vector)
    # end = time.time()
    # print(f"Time elapsed: {end - start} seconds")
    #
    # start = time.time()
    # print(pathList[91])
    # vector, y, sr = (TempoEstimator.getTempoVector(pathList[91]))
    # print(vector)
    #
    # with Pool(12) as p:
    #     for result in p.imap(TempoGetter.getRawTempo, pathList):
    #         print(result)
    #
    Tempo_from_Tempo()
    end = time.time()

    print(f"Time elapsed: {end - start} seconds")

    # print(TempoEstimator.DynamicTempoAlgo(pathList[2]))
    # print(TempoGetter.get_Dtempo(pathList[2], sr_multiplier= 4, starting_tempo= 160))
    # TempoEstimator.combinedAlgo(pathList)
