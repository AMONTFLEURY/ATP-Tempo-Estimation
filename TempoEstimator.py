import multiprocessing

import librosa
from numba.cuda.libdeviceimpl import args

import TempoGetter
from multiprocessing import Pool, Queue
import SystemManager
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import statistics as stats

from TempoGetter import getRawTempo


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
    if path != "":
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
            # else:
            #     if holder[-1][0] - holder[tempo2][0] - 20 > 15:
            #         tempo3 = len(holder) - 2
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


def process_1(y, sr, path="", q=None):
    q.put(TempoGetter.getRawTempo(mp3Path=path, y=y, sr=sr * 0.5))


def process_2(y, sr, path="", q=None):
    q.put(TempoGetter.getRawTempo(mp3Path=path, y=y, sr=sr))


def process_3(y, sr, path="", q=None):
    q.put(TempoGetter.get_tempo_from_onset(mp3Path="", y=y, sr=sr))


def process_4(y, sr, path="", q=None):
    q.put(DynamicTempoAlgo(path, y, sr))


def process_5(y, sr, path="", q=None):
    holder, tempo1, tempo2, tempo3 = DTA_Getter(path, y, sr)
    q.put([holder[tempo1][1], holder[tempo2][1]])


def getTempoVectorMP(path):
    y, sr = librosa.load(path, sr=None, mono=True)
    q = Queue()
    p1 = multiprocessing.Process(target=process_1, args=(y, sr, path, q))
    p2 = multiprocessing.Process(target=process_2, args=(y, sr, path, q))
    p3 = multiprocessing.Process(target=process_3, args=(y, sr, path, q))
    # p4 = multiprocessing.Process(target=process_4, args=(y, sr, path, q))
    p5 = multiprocessing.Process(target=process_5, args=(y, sr, path, q))

    p1.start()
    p2.start()
    p3.start()
    # p4.start()
    p5.start()

    results = []
    for i in range(4):
        results.append(q.get())

    p1.join()
    p2.join()
    p3.join()
    # p4.join()
    p5.join()

    vectorU = results
    return vectorU


def getTempoVector(path):
    y, sr = librosa.load(path, sr=None, mono=True)
    vector = [0]
    vector.append(TempoGetter.getRawTempo(path, y=y, sr=sr * 0.5))
    vector.append(TempoGetter.getRawTempo(path, y=y, sr=sr))
    vector.append(TempoGetter.getRawTempo(path, y=y, sr=sr * 2))

    vector.append(TempoGetter.get_tempo_from_onset(mp3Path=" ", y=y, sr=sr))

    x1, x2 = TempoGetter.Tempo_TimeFrame(path=path)
    vector.append(x1)
    vector.append(x2)

    # vector.append(DynamicTempoAlgo(path, y, sr))
    # vector.append(TempoGetter.getRawTempo(path, y=y, sr=sr * 0.33))

    holder, tempo1, tempo2, tempo3 = DTA_Getter(path, y, sr)
    vector.append(holder[tempo1][1])
    vector.append(holder[tempo2][1])

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
