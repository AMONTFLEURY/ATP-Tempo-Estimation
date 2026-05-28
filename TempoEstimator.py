import librosa
import TempoGetter
from multiprocessing import Pool
import SystemManager
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def estimate(path, threading=False):
    if type(path).__name__ == "str":
        # load track, 1
        return estimate_single_track(path)
        # print("String arg")
    elif type(path).__name__ == "list":
        list_with_MP(path)
        if type(path[0]).__name__ == "list":
            print("List of list arg")


def list_with_MP(list_of_paths=None):
    # list_of_list = SystemManager.splitPathList(list_of_paths)
    # with Pool(2) as p:
    #     (p.map(estimate_single_track, list_of_paths))
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
        return "Failed Test for " + path


def getDummyTempo(tempo):
    if tempo >= 140 and tempo % 2 == 0:
        return tempo / 2
    elif tempo <= 80:
        return tempo * 2
