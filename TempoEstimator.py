import math
import multiprocessing

import librosa
from numba import double
from numba.cuda.libdeviceimpl import args
from numpy import dtype

import RefTableManager
import RoundChecker
import TempoGetter
from multiprocessing import Pool, Queue
import SystemManager
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import statistics as stats
import pandas as pd

import TempoStabilityUnit
from TempoGetter import getRawTempo
from UDManager import df


def estimate(path, threading=False):
    if type(path).__name__ == "str":
        # load track, 1
        return estimate_single_track(path)
        # print("String arg")
    elif type(path).__name__ == "list":
        if type(path[0]).__name__ == "list":
            print("List of list arg")
        else:
            with Pool(6) as p:
                for result in p.imap(estimate_single_track, path):
                    print(result)


def list_with_MP(list_of_paths=None):
    list_of_list = SystemManager.splitPathList(list_of_paths)
    with Pool(2) as p:
        (p.map(estimate_single_track, list_of_paths))
    pass


def list_no_MP(path):
    pass


def estimate_single_track(path):
    y, sr = librosa.load(path, sr=None, mono=True, duration=120, offset=30)
    tempo0 = TempoGetter.getRawTempo(y=y, sr=sr, srm=0.5)
    dynam_tempo_array0, all_dTypos0 = TempoGetter.get_Dtempo(path, sr_multiplier=2,
                                                             onset=True, starting_tempo=tempo0, interval=200)
    avg_dev0 = SystemManager.get_average_deviation(dynam_tempo_array0)
    dynam_tempo_array1, all_dTypos1 = TempoGetter.get_Dtempo(path, sr_multiplier=2,
                                                             onset=False, starting_tempo=tempo0, interval=200)
    avg_dev1 = SystemManager.get_average_deviation(dynam_tempo_array1)
    dummyTempo = getDummyTempo(round(tempo0))
    mode, mode_count = SystemManager.compareDynamicTempos(dynam_tempo_array0, dynam_tempo_array1)
    print(path)
    print(mode_count / len(dynam_tempo_array1))
    if avg_dev0 <= 0.1 and avg_dev1 <= 0.1 and 0.70 <= (mode_count / len(dynam_tempo_array0)):
        return mode
    else:
        return -1


def getDummyTempo(tempo):
    if tempo >= 140 and tempo % 2 == 0:
        return tempo / 2
    elif tempo <= 80:
        return tempo * 2


def getTempoFromDynamTempoArray(path, tempo=120, onset=False, sr=1):
    dynam_tempo_array0, all_dTypos0 = TempoGetter.get_Dtempo(mp3Path=path, onset=onset, sr_multiplier=sr,
                                                             starting_tempo=tempo, interval=200)
    avg_dev0 = SystemManager.get_average_deviation(dynam_tempo_array0)
    mode, mode_count = SystemManager.compareDynamicTempos(dynam_tempo_array0, dynam_tempo_array0)
    return mode, round(float(avg_dev0), 4)


def DynamicTempoAlgo(path="", y=None, sr=None):
    holder, tempo1, tempo2, tempo3 = DTA_Getter(path, y=y, sr=sr)
    estimated = DTA_Analyzer(holder, tempo1, tempo2, tempo3, path, y=y, sr=sr)
    return estimated


def DTA_Getter(path="", y=None, sr=None):
    # print(path)
    if path == "":
        y, sr = librosa.load(path, mono=True, sr=None)

    # each cell of the holder includes [Initial/Starting Tempo, Mode, Average Deviation]
    holder = []
    starting_tempo = 40
    increment = 5
    tempo1, tempo2, tempo3 = 0, 0, 1

    # intailizing the holder array for the while loop to work
    dynam_tempo_array0, all_dTypos0 = TempoGetter.get_Dtempo(mp3Path=path, sr=sr, y=y, onset=False, sr_multiplier=1,
                                                             starting_tempo=starting_tempo, interval=200)
    # Gets average deviation
    avg_dev0 = SystemManager.get_average_deviation(dynam_tempo_array0)
    # just to get the mode
    mode = stats.mode(dynam_tempo_array0)
    holder.append([starting_tempo, mode, avg_dev0])
    # While start
    while tempo1 == 0 or tempo2 == 0 or tempo3 == 0:
        starting_tempo += increment
        dynam_tempo_array0, all_dTypos0 = TempoGetter.get_Dtempo(mp3Path=path, sr=sr, y=y, onset=False,
                                                                 sr_multiplier=0.5,
                                                                 starting_tempo=starting_tempo, interval=200)
        avg_dev0 = SystemManager.get_average_deviation(dynam_tempo_array0)
        mode = stats.mode(dynam_tempo_array0)
        holder.append([starting_tempo, mode, avg_dev0])

        # Checks if the latest holder in the cell is greater than the previous
        # if it is then the previous cell has the is at the lowest point and
        # that index will be stored,

        if holder[-1][2] > holder[-2][2] and holder[-1][0] - holder[tempo1][0] > 10:
            if tempo1 == 0:
                tempo1 = len(holder) - 2
                starting_tempo += 15
            elif tempo2 == 0:
                if holder[-1][0] - holder[tempo1][0] - 20 > 15:
                    tempo2 = len(holder) - 2
                    starting_tempo += 15

    return holder, tempo1, tempo2, tempo3


def DTA_Analyzer(holder, tempo1, tempo2, tempo3, path, y=None, sr=None):
    onset_tempo = TempoGetter.get_tempo_from_onset(path, sr_multiplier=1, y=y, sr=sr)
    estimated_tempo = -2
    if holder[tempo2][1] % holder[tempo1][1] == 0 and (holder[tempo2][2] < 0.85 or holder[tempo2 - 1][2] < 0.85):
        estimated_tempo = holder[tempo2][1]
        if holder[tempo1][2] == 0.0 and holder[tempo2][1] % holder[tempo2][0] == 1:
            return holder[tempo2][0]
        else:
            return estimated_tempo

    # Rounding check
    if holder[tempo2][1] % 10 == 1 or holder[tempo2][1] % 10 == 9:
        if (holder[tempo2][1] - 1) % (holder[tempo1][1]) == 0:
            estimated_tempo = holder[tempo2][1] - 1
        elif (holder[tempo2][1] + 1) % (holder[tempo1][1]) == 0:
            estimated_tempo = holder[tempo2][1] + 1

        elif (holder[tempo2][1] - 1) % (holder[tempo1][1] - 1) == 0:
            estimated_tempo = holder[tempo2][1] - 1
        elif (holder[tempo2][1] + 1) % (holder[tempo1][1] + 1) == 0:
            estimated_tempo = holder[tempo2][1] + 1
        # DOES THIS NEED A CHECK?

        elif (holder[0][1] - 1) % (holder[tempo1][1] - 1) == 0:
            estimated_tempo = holder[tempo2][1] - 1
        elif (holder[tempo2][1] + 1) % (holder[tempo1][1] + 1) == 0:
            estimated_tempo = holder[tempo2][1] + 1

        if estimated_tempo < 0:
            if onset_tempo - 0.7 < holder[tempo2][1] < onset_tempo + 0.7:
                return holder[tempo2][1]
            else:
                # y, sr = librosa.load(path)
                tempo, beats = librosa.beat.beat_track(y=y, sr=sr * 2, start_bpm=holder[tempo2][1])
                tempo = round(tempo[0])

                if tempo - 0.7 < holder[tempo2][1] < tempo + 0.7 or tempo - 0.7 < (holder[tempo2][1] / 2) < tempo + 0.7:
                    # or (holder[tempo2][1] + 1) % (tempo + 1) == 0:
                    if (holder[tempo1][1] - 1) % (tempo - 1) == (holder[tempo1][1] - 1):
                        estimated_tempo = (holder[tempo1][1] - 1)
                    elif (tempo + 1) % (holder[tempo1][1] - 1) == (holder[tempo1][1] - 1):
                        estimated_tempo = (holder[tempo1][1] + 1)
        return estimated_tempo


    else:
        if onset_tempo - 0.7 < holder[tempo2][1] < onset_tempo + 0.7:
            return holder[tempo2][1]
        elif (onset_tempo - 0.7) / 2 < holder[tempo1][1] < (onset_tempo + 0.7) / 2:
            if onset_tempo - 0.5 < (holder[tempo1][1] * 2) < onset_tempo + 0.5:
                mode, ave_de = getTempoFromDynamTempoArray(path, tempo=holder[tempo1][1] * 2)
                if ave_de < 0.2 or mode % holder[tempo1][1] == 0:
                    # y, sr = librosa.load(path)
                    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, start_bpm=holder[tempo2][1])
                    if tempo - 0.7 < holder[tempo2][1] < tempo + 0.7 or tempo - 0.7 < (
                            holder[tempo2][1] / 2) < tempo + 0.7:
                        return holder[tempo2][1]
                    else:
                        estimated_tempo = -1.1
                else:
                    estimated_tempo = -1.2
            else:
                mode, ave_de = getTempoFromDynamTempoArray(path, tempo=holder[tempo2][1], onset=True, sr=2)
                mode2, ave_de2 = getTempoFromDynamTempoArray(path, tempo=holder[tempo2][1], sr=2)
                if mode == mode2:
                    return mode
                else:
                    estimated_tempo = -3

    return estimated_tempo


def checkBeatTiming(path, estimated_tempo, tempo2):
    y, sr = librosa.load(path)
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, start_bpm=estimated_tempo)
    beats = librosa.frames_to_time(beats, sr=sr)
    estimated_tempo += 2
    x = (beats[estimated_tempo] - beats[0])
    x2 = (beats[estimated_tempo / 2] - beats[estimated_tempo])
    print(x, x2)

    while x > 60 and x2 > 30:
        estimated_tempo -= 1
        x = (beats[estimated_tempo] - beats[0])
        x2 = (beats[estimated_tempo * 2] - beats[estimated_tempo])
    print(x, x2)
    return estimated_tempo + 1


# def addToGrid(arg, i):
#     base[i].append(arg)


#
def crossChecker(array, dummy, weight=2):
    weight = -weight
    if array[3] < 0:
        if dummy[0] == array[0]:
            weight += 1
        if dummy[1] == array[1]:
            weight += 1
        if dummy[2] == array[2]:
            weight += 2
    if weight >= 0:
        return dummy[3]
    else:
        return array[3]


def DTA_checker(array, y, sr):
    if array[3] < 0:
        tempo = TempoGetter.estimate_Tempo_From_Tempo(y=y, sr=sr, tempo=array[0])
        x1, x2 = TempoGetter.getBeatTime(y=y, sr=sr)
        if x1 > 60 and x2 > 60:
            tempo += 1
        elif x1 < 60 and x2 > 60:
            tempo -= 1
        return tempo
    else:
        return -9



# Get sampling vectors form librosa, Compute heavy
def getTempoVector(path, chunk=None):
    if chunk == None:
        y, sr = librosa.load(path, sr=None, mono=True)
    else:
        if chunk < 0:
            y, sr = librosa.load(path, sr=None, mono=True, duration= -chunk)
        else:
            y, sr = librosa.load(path, sr=None, mono=True, offset=chunk)

    vector = [0]
    vector.append(TempoGetter.getRawTempo(path, y=y, sr=sr * 0.5))
    vector.append(TempoGetter.getRawTempo(path, y=y, sr=sr))
    vector.append(TempoGetter.getRawTempo(path, y=y, sr=sr * 2))

    vector.append(TempoGetter.get_tempo_from_onset(mp3Path=" ", y=y, sr=sr))

    x1, x2 = TempoGetter.Tempo_TimeFrame(path=path)
    vector.append(x1)
    vector.append(x2)

    holder, tempo1, tempo2, tempo3 = DTA_Getter(path, y, sr)
    vector.append(holder[tempo1][1])
    vector.append(holder[tempo2][1])
    # print(vector)

    return vector, y, sr


def combinedAlgo(path_list):
    base = []
    for i in range(len(path_list)):
        base.append([])
    # for path in path_list:
    #     base.append([path])
    for i in range(len(path_list)):
        base[i].append(TempoGetter.getRawTempo(path_list[i], srm=0.5))
        base[i].append(TempoGetter.getRawTempo(path_list[i]))
        base[i].append(TempoGetter.get_tempo_from_onset(path_list[i], ))
    for i in range(len(path_list)):
        base[i].append(DynamicTempoAlgo(path_list[i]))
    for i in range(len(path_list)):
        estimate_single_track(path_list[i])
    for i in range(len(path_list)):
        TempoGetter.get_onsets(path_list[i], startBPM=base[i])


# def scorer(row):
#     if
#     pass


# searches for best match in reference slice by evaluating each reference point,
# then picking the point with the best score, only exact matches give points
def cross_finder(vector, slice):
    # print(slice)
    cur_score = 0
    current_tempo = slice.iloc[0, 0]
    round_bias = "up"
    for row in slice.itertuples():
        score = 0
        if row._2 == vector[1]:
            score += 1
        if row._3 == vector[2]:
            score += 1.2
        if row._4 == vector[3]:
            score += 1
        if row._5 == vector[4]:
            score += 1
        if row._6 == vector[5]:
            score += 1
        if row._7 == vector[6]:
            score += 1.2
        if row.DTF1 == vector[7]:
            score += 1
        # Could be Removed
        if row._4 == vector[3]:
            score += .2
        if row.DTF2 == vector[8]:
            score += 1
        if cur_score <= score:
            # If the winning score is giving to the wrong Tempo,
            # the algo knows that it must be the previous Tempo or between
            # Better way of doing rounding checks
            if cur_score == score and score != 0:
                round_bias = "down"
            current_tempo = row.Tempo
            cur_score = score
    return current_tempo, cur_score, round_bias


# Take sample vector, to estimate tempo,
# Heart of algorithm
def cross_checker(vector):
    tempo1, score1 = None, None
    estimated_tempo = TempoStabilityUnit.slice_correcter([vector[1], vector[2], vector[3]])
    # if estimated_tempo
    slice0, slice1 = RefTableManager.get_table_slices(estimated_tempo)
    # print(type(slice0), type(slice1))
    tempo0, score0, round_bias0 = cross_finder(vector, slice0)
    if slice1 is not None:
        tempo1, score1, round_bias1 = cross_finder(vector, slice1)
    return [tempo0, tempo1], [score0, score1], round_bias0


# I/O for Algorithm
def cross_estimation(path):
    print(path)
    vector, y, sr = getTempoVector(path)
    tempo, score, round_bias0 = cross_checker(vector)
    tempo = RoundChecker.check(tempo, score, round_bias0)
    if sum(score) < 5:
        print("Checking for stability... ->", path)
        tempo[0], score[0] = TempoStabilityUnit.stability_check(y, sr, path, tempo)
    if tempo[1] is None or tempo[0] is None:
        if tempo[0] is None:
            tempo[0] = tempo[1]
        message = (f"Estimated tempo: {tempo[0]}"
                   f"\nScore 1: {score[0]}")
    else:
        message = (
            f"Estimated tempo: {tempo[0]} with a double/half time of: {tempo[1]}"
            f"\nScore 1: {score[0]}"
            f"\nScore 2: {score[1]}")

    # if tempo[1] is not None and tempo[0] == tempo[1]:
    #     if tempo[0] is None and tempo[0] != tempo[1]:
    #         tempo[0] = tempo[1]
    #     message = (
    #         f"Estimated tempo: {tempo[0]} with a double/half time of: {tempo[1]}"
    #         f"\nScore 1: {score[0]}"
    #         f"\nScore 2: {score[1]}")
    # else:
    #     RoundChecker.rolling_star(score, tempo)
    #     message = (f"Estimated tempo: {tempo[0]}"
    #                f"\nScore 1: {score[0]}")
    # print('\n')
    vector[0] = tempo[0]
    return vector, message
